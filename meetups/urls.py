from django.urls import path

from . import views
from .views import *


urlpatterns = [
    path('', MeetupHome.as_view(), name='meetups'),  # domain.com/meetups
    path('new-meetup', NewMeetup.as_view(), name='new-meetup'),
    path('<slug:meetup_slug>/new-visitor', views.confirm_registration, name='new-visitor'),
    path('<slug:meetup_slug>', MeetupDetails.as_view(), name='meetup-detail'),
]
