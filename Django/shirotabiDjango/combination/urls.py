from django.urls import path
from .views import *
urlpatterns = [
     path(route='',view= IndexView.as_view(),name = 'index'),
]
