from . import views
from . import webhook
from django.conf.urls import url

urlpatterns = [
    url(r'fb', webhook.FBWebhook.as_view()),
    url(r'wallet', views.view_wallet, name='view_wallet'),
]