from functools import wraps
from datetime import datetime
import sys

from serial import Serial

from django.core.management.base import BaseCommand

from ...models import TempHistory, TempSettings

class TimeoutException(Exception):
    pass

def timeout_exception(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        res = f(*args, **kwds)
        if not res:
            raise TimeoutException()
        return res
    return wrapper

Serial.read = timeout_exception(Serial.read)

class Command(BaseCommand):
    args = '</dev/ttyPORT> <baudrate>'
    help = 'Reads temperature data from thermostat device, writes current boundaries'

    def handle(self, *args, **options):
        if len(args) < 2:
            print "No enough arguments"
            return

        n = 0
        MAX = 5
        while(n < MAX):
            try:
                ser = Serial(args[0], args[1], timeout=5)
                ser.write('t')
                temp = float(ser.readline()[:-1]) / 10
                ser.write('c')
                state = ser.read()
                TempHistory.objects.create(datetime=datetime.utcnow(), temp=temp, state=state)

                settings = TempSettings.load()
                ser.write('sl{:d} '.format(int(settings.low_boundary * 10)))
                ser.write('sh{:d} '.format(int(settings.high_boundary * 10)))
            except TimeoutException:
                ser.close()
                n += 1
            else:
                break
        if n == MAX:
            sys.stdeff.write('Error syncing with thermostat')
