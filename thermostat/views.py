from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages

from .forms import TempSettingsForm
from .models import TempSettings, TempHistory


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
