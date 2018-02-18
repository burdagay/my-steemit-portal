from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'fb', views.FBWebhook.as_view()),
]