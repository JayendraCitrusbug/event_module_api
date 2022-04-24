from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    username = models.ForeignKey(User, on_delete=models.PROTECT)
    event_name = models.CharField(max_length=70)
    event_address = models.CharField(max_length=70)
    organiser_name = models.CharField(max_length=70)
    organiser_email = models.CharField(max_length=70)
    event_created_at = models.DateTimeField(auto_now_add=True)
    event_updated_at = models.DateTimeField(auto_now=True)
    event_active = models.BooleanField(default=False)

    def __str__(self):
        return self.event_name
        

class TimeLapse(models.Model):
    time_lapse = models.TimeField()

    def __str__(self):
        return str(self.time_lapse)


class EventDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    event_date = models.DateField()
        
    def __str__(self):
        return str(self.event_date)


class AccessPoint(models.Model):
    accesspoint_name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.accesspoint_name)


class EventSlot(models.Model):
    time_lapse = models.ForeignKey(TimeLapse, on_delete=models.CASCADE)
    event_date = models.ForeignKey(EventDate, on_delete=models.CASCADE)
    accesspoint = models.ForeignKey(AccessPoint, on_delete=models.CASCADE, null=True, blank=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.time_lapse)


class SlotAccessPoint(models.Model):
    event_slot = models.ForeignKey(EventSlot, on_delete=models.CASCADE)
    accesspoint = models.ForeignKey(AccessPoint, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.event_slot)