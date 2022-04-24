import datetime
from .models import *
from django import views
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .tasks import expired_event_delete_func, sendgrid_mail



class EventAPI(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # @csrf_exempt

    def get(self,request):
        try:
            event = Event.objects.get(pk=request.GET.get('filter'))
            eventserializer = EventSerializer(event)
            date = EventDate.objects.filter(event__event_name=event)
            dateserializer = EventDateSerializer(date, many=True)
            accesspoints = EventSlot.objects.filter(event_date__event=event).values_list('accesspoint__accesspoint_name', flat=True).distinct()
        except:
            return Response("Details for this event not found...!")
        serializer = [eventserializer.data, dateserializer.data, sorted(list(accesspoints))]
        sendgrid_mail(serializer)
        return Response(serializer)


    def post(self, request):
        event_name = request.data['event_name']
        event_address = request.data['event_address']
        organiser_name = request.data['organiser_name']
        organiser_email = request.data['organiser_email']
        data = request.data['data']

        eventdate = [data[i]['date'] for i in range(len(data))]
        totalslots = [TimeLapse.objects.filter(time_lapse__range=[data[i]['start_slot'], data[i]['end_slot']]) for i in range(len(data))]


        event = Event.objects.create(username=request.user, event_name=event_name, event_address=event_address, organiser_name=organiser_name, organiser_email=organiser_email)
        event_date = EventDate.objects.bulk_create(EventDate(event=event, event_date=i)for i in eventdate)
        eventslot = EventSlot.objects.bulk_create(EventSlot(
                                                            time_lapse=TimeLapse.objects.filter(time_lapse=str(k)).first(),
                                                            event_date=EventDate.objects.filter(event_date=data[i].get('date')).first(),
                                                            accesspoint=AccessPoint.objects.get(id=j))
                                                            # accesspoint=AccessPoint.objects.get(id=AccessPoint.objects.get(id=j, is_active=True).pk))
                                                            for i in range(len(data))
                                                            for j in data[i].get('access_points') for k in totalslots[i])
        
        slotaccesspoint = SlotAccessPoint.objects.bulk_create(SlotAccessPoint(
                                                                    event_slot = i,
                                                                    accesspoint = AccessPoint.objects.filter(accesspoint_name=i.accesspoint).first())
                                                                    for i in eventslot)


        serializer = EventSerializer(event)
        return Response(serializer.data)



class BookSlotAPI(ListAPIView):
    def post(self, request):
        event_id = request.data['event_id']
        slot_id = request.data['slot_id']
        
        if Event.objects.filter(pk=request.data['event_id']):
            slots = EventSlot.objects.filter(pk=slot_id)
            if slot:
                for slot in slots:
                    slot.is_booked = True
                    slot.save()
            else:
                return Response("Slot for this event not found...!")
        else:
            return Response("Event with this ID not found...!")
        return Response({"event_id":event_id, "slot_id":slot_id})
        


class AvailableSlotAPI(ListAPIView):
    def get(self, request):
        available_slots = EventSlot.objects.filter(is_booked=False, event_date__event__pk=request.GET.get('filter')).values('id')
        return Response(available_slots)



def test(request):
    expired_event_delete_func()
    return HttpResponse("done")

