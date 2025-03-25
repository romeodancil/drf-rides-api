from django.urls import path

from . import views
from . import userview

urlpatterns = [
    path("", views.index, name="index"),
    path("/user", userview.UserView.as_view(), name="user_view"),
    path('/api/token/', userview.get_user_token, name='get_user_token'),
]