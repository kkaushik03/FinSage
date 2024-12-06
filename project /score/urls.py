from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Root URL serves the HTML
    path('api/hello/', views.hello_world, name='hello_world'),  # API endpoint
]