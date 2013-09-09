from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from singleton import SingletonModel


class TempHistory(models.Model):
    datetime = models.DateTimeField(verbose_name='Date-time')
    temp = models.FloatField(verbose_name='Temperature')
    state = models.CharField(max_length=1, verbose_name='Boiler state', help_text='1 - on, 0 - off')

    def __unicode__(self):
        return "{}, temp {:.2f}, state '{}'".format(self.datetime, self.temp, self.state)

    @classmethod
    def cur_temp(cls):
        try:
            return cls.objects.order_by('-datetime')[0].temp
        except IndexError:
            return "No data"

    @classmethod
    def cur_state(cls):
        try:
            return cls.objects.order_by('-datetime')[0].state
        except IndexError:
            return "No data"

    class Meta:
        verbose_name = 'Temperature history record'
        verbose_name_plural = 'Temperature history records'


class TempSettings(SingletonModel):
    low_boundary = models.FloatField(verbose_name='Low boundary', default=21.5)
    high_boundary = models.FloatField(verbose_name='High boundary', default=22.0)

    def __unicode__(self):
        return "Temperature settings"

    class Meta:
        verbose_name = 'Temperature settings'
        verbose_name_plural = 'Temperature settings'


class TempSettingsHistory(models.Model):
    low_boundary = models.FloatField(verbose_name='Low boundary')
    high_boundary = models.FloatField(verbose_name='High boundary')
    datetime = models.DateTimeField(verbose_name='Date-time', auto_now_add=True)

    def __unicode__(self):
        return "Low {:.2f}, High {:.2f}, Date {}'".format(self.low_boundary, self.high_boundary, self.datetime)

    class Meta:
        verbose_name = 'Temperature settings history record'
        verbose_name_plural = 'Temperature settings history records'


@receiver(post_save, sender=TempSettings)
def save_history(**kwargs):
    TempSettingsHistory.objects.create(
        low_boundary=kwargs["instance"].low_boundary,
        high_boundary=kwargs["instance"].high_boundary
    )
