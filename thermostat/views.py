import json
import datetime
import dateutil.parser
import dateutil.zoneinfo
from dateutil.tz import tzutc

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse

from .forms import TempSettingsForm
from .models import TempSettings, TempHistory, TempSettingsHistory


def control(request):
    if request.method == "POST":
        form = TempSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "New boundaries have been stored")
    else:
        form = TempSettingsForm(instance=TempSettings.load())
    data = {
        "form": form,
        "cur_temp": TempHistory.cur_temp(),
        "cur_state": TempHistory.cur_state(),
    }
    return render_to_response("control.html", data,
                              context_instance=RequestContext(request))


def graph(request):
    return render_to_response("graph.html", {},
                              context_instance=RequestContext(request))


class _DateTimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        else:
            return super(_DateTimeJSONEncoder, self).default(obj)


def _dumpjson(data):
    return json.dumps(data, cls=_DateTimeJSONEncoder)


def graph_data(request):
    import datetime  # TODO: why import in the beginning of file doesn't work?
    begin = request.GET.get("begin")
    end = request.GET.get("end")
    tz = request.GET.get("tz")

    begin = dateutil.parser.parse(begin).replace(tzinfo=None)  # to naive datetime for SQLite
    end = dateutil.parser.parse(end).replace(tzinfo=None)
    tz = dateutil.zoneinfo.gettz(tz)
    points = list(TempHistory.objects.filter(datetime__gte=begin, datetime__lte=end).order_by('datetime')
                  .values('datetime', 'temp', 'state'))

    boundaries = list(TempSettingsHistory.objects.filter(datetime__gte=begin, datetime__lte=end).order_by('datetime')
                      .values('datetime', 'low_boundary', 'high_boundary'))
    bound_before = TempSettingsHistory.objects.order_by('-datetime').filter(datetime__lt=begin)
    if len(bound_before) > 0:
        boundaries.insert(0, bound_before[0:1]
                          .values('datetime', 'low_boundary', 'high_boundary')[0])  # TODO: optimize?
    else:
        settings = TempSettings.load()
        boundaries.insert(0, {
            'datetime': begin - datetime.timedelta(seconds=1),
            'low_boundary': settings.low_boundary,
            'high_boundary': settings.high_boundary,
        })

    utc = tzutc()
    for item in points:
        item['datetime'] = item['datetime'].replace(tzinfo=utc).astimezone(tz)
    for item in boundaries:
        item['datetime'] = item['datetime'].replace(tzinfo=utc).astimezone(tz)

    heating_periods = []
    prev = start = end = None
    for point in points:
        if prev:
            if point['state'] == '0':
                heating_periods.append({'startValue': start, 'endValue': end})
                prev = start = None
        else:
            if point['state'] == '1':
                start = point['datetime']
                prev = True
        end = point['datetime']
    if start and end:
        heating_periods.append({'startValue': start, 'endValue': end})

    # thin out array
    MAX_POINTS = 100
    cur_boundary_i = 0
    if len(points) > MAX_POINTS:
        ratio = len(points) // MAX_POINTS
        thinout_points = []
        for i in range(len(points) // ratio):
            datetime = points[i * ratio + ratio // 2]['datetime']
            temp = 0
            for item in points[i * ratio:(i + 1) * ratio]:
                temp += item['temp']
            temp /= ratio
            temp = round(temp, 2)
            if cur_boundary_i + 1 < len(boundaries):
                if boundaries[cur_boundary_i + 1]['datetime'] <= datetime:
                    cur_boundary_i += 1
            thinout_points.append({'datetime': datetime, 'temp': temp,
                                   'low_boundary': boundaries[cur_boundary_i]['low_boundary'],
                                   'high_boundary': boundaries[cur_boundary_i]['high_boundary']})
        points = thinout_points

    data = {
        'heating_periods': heating_periods,
        'points': points,
    }
    return HttpResponse(_dumpjson(data), content_type='application/json')
