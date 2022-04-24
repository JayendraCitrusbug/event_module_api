import email
from urllib import response
from celery import shared_task
from .models import *
import datetime
from django.core.mail import send_mail


@shared_task(bind=True)
def expired_event_delete_func(self):
    event = Event.objects.all()
    eventdate = EventDate.objects.all()
    for i in event:
        ed = eventdate.filter(event=i)
        value_list = sorted(ed.values_list('event_date', flat=True))
        last_date = value_list[len(value_list)-1]

        event_last_dated = eventdate.get(event_date=last_date, event__id=i.id)
        last_event_date = event_last_dated.event_date
        if last_event_date<datetime.datetime.now().date():
            event.filter(id=event_last_dated.event.id).delete()
    return "Done...!"
    

import sendgrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from event_module.settings import SENDGRID_API_KEY

@shared_task(bind=True)
def sendgrid_mail(self, serializer):
    message = Mail(from_email="jayendra.citrusbug@gmail.com",
                    to_emails="jayendraiant@gmail.com",
                    subject="Sending with SendGrid is fun...!",
                    plain_text_content="and easy to do anywhere, even with Python.")
    message.dynamic_template_data={"organiser_name":serializer[0].get('organiser_name'),
                                    "event_name":serializer[0].get('event_name'),
                                    "event_address":serializer[0].get('event_address'),
                                    "dates":serializer[1],
                                    "access_points":serializer[2]}
    message.template_id='d-a0df076a5ece4aa0849c8155d3bd9b7f'
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
