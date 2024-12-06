from django.urls import path
from . import views

urlpatterns = [
    path('', views.process_input, name='index'),  # Main page URL
]