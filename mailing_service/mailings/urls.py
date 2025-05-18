from django.urls import path
from .views import MailingListView, MailingCreateView

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
]
