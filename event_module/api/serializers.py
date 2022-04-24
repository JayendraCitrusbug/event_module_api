from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['event_name', 'event_address', 'organiser_name', 'organiser_email']

class EventDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDate
        fields = ['event_date']

class AccessPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessPoint
        fields = "__all__"

class EventSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSlot
        fields = "__all__"


# class DetailsSerializer(serializers.ModelSerializer):

#     date = serializers.SerializerMethodField('get_date')
#     accesspoints = serializers.SerializerMethodField('get_accesspoints')

#     def get_date(self, event):
#         serializer = EventDateSerializer(EventDate.objects.filter(event__event_name=event), many=True)
#         return serializer.data
    
#     def get_accesspoints(self, event):
#         # serializer = AccessPointSerializer(EventSlot.objects.filter(event_date__event=event).values_list('accesspoint__accesspoint_name', flat=True).distinct(), many=True)
#         serializer = AccessPointSerializer()
#         return serializer.data

#     class Meta:
#         model = Event
#         fields = ['event_name', 'event_address', 'organiser_name', 'organiser_email', 'date', 'accesspoints']


