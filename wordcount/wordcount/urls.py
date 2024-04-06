from django.urls import path
from .views import WordCountAPIView

urlpatterns = [
    path('wordcount/', WordCountAPIView.as_view(), name='wordcount'),
]
