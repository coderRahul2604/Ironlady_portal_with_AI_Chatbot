from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_page, name='chat-page'),
    path('ask/', views.ask, name='chat-ask'),   # AJAX POST endpoint
]
