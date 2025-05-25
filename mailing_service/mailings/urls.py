from django.urls import path
from .views import MailingListView, MailingCreateView, HomeView

app_name = 'mailings'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('', MailingListView.as_view(), name='mailing_list'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
]
