from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Event)
@admin.register(Event)
class EventTableAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'event_name', 'event_address', 'organiser_name', 'organiser_email', 'event_created_at', 'event_updated_at', 'event_active']

@admin.register(TimeLapse)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ['time_lapse']

@admin.register(EventDate)
class EventDateTableAdmin(admin.ModelAdmin):
    list_display = ['event', 'event_date']
    
@admin.register(AccessPoint)
class AccessPointTableAdmin(admin.ModelAdmin):
    list_display = ['accesspoint_name', 'is_active']
    
@admin.register(EventSlot)
class EventSlotTableAdmin(admin.ModelAdmin):
    list_display = ['time_lapse', 'event_date', 'accesspoint', 'is_booked']

@admin.register(SlotAccessPoint)
class SlotAccessPointsTableAdmin(admin.ModelAdmin):
    list_display = ['event_slot', 'accesspoint']