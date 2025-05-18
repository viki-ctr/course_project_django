from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from mailings.models import Mailing, MailingAttempt

class Command(BaseCommand):
    help = 'Send scheduled mailings'

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status='started')
        for mailing in mailings:
            for recipient in mailing.recipients.all():
                try:
                    send_mail(
                        mailing.message.subject,
                        mailing.message.body,
                        'noreply@example.com',
                        [recipient.email],
                    )
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status='success',
                        server_response='OK',
                    )
                except Exception as e:
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status='failed',
                        server_response=str(e),
                    )
