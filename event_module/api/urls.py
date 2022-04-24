from django.urls import path, include
from . import views

urlpatterns = [
    path('event/', views.EventAPI.as_view(), name='event'),
    path('bookslot/', views.BookSlotAPI.as_view(), name='bookslot'),
    path('availableslot/', views.AvailableSlotAPI.as_view(), name='availableslot'),
    path('celery/', views.test, name='celery'),
]