from django.urls import path
from .views import home

app_name = 'chatbot'

urlpatterns = [
    path('', home, name='inicio'),
]
