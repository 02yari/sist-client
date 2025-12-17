from django.urls import path
<<<<<<< HEAD
from .views import home

app_name = 'chatbot'

urlpatterns = [
    path('', home, name='inicio'),
=======
from .views import chatbot

urlpatterns = [
    path('chatbot/', chatbot, name='chatbot'),
>>>>>>> 5b34b49df5170eb9918c1e83213a49a72b55b318
]
