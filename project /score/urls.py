from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Render the homepage
    path('api/hello/', views.hello_world, name='hello_world'),  # API endpoint
    path('process_input/', views.process_input, name='process_input'),  # Handle user input
]