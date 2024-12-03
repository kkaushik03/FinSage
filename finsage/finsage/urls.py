from django.urls import path
from financial.views import parse_document  # Adjust 'financial' to match your app name

urlpatterns = [
    path('parse-document/', parse_document, name='parse_document'),
]