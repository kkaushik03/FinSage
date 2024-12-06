from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Homepage view
    path('process_input/', views.process_input, name='process_input'),  # Process input
]