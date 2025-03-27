from django.urls import path

from . import views
from . import userview, ridesview

urlpatterns = [
    path("", views.index, name="index"),
    path("user", userview.UserView.as_view(), name="user_view"),
    path("ride", ridesview.RidesView.as_view(), name="rides"),
    path("ride-events", ridesview.RidesEvents.as_view(), name="ride_events"),
    path('api/token/', userview.get_user_token, name='get_user_token'),
]