from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from mailing_service.mailings.models import Mailing, MailingAttempt


class Command(BaseCommand):
    help = 'Отправляет запланированные рассылки'

    def handle(self, *args, **options):
        now = timezone.now()
        mailings = Mailing.objects.filter(
            status='started',
            start_time__lte=now,
            end_time__gte=now
        )

        for mailing in mailings:
            self.stdout.write(f'Обработка рассылки #{mailing.id}')

            for recipient in mailing.recipients.all():
                try:
                    send_mail(
                        mailing.message.subject,
                        mailing.message.body,
                        settings.DEFAULT_FROM_EMAIL,
                        [recipient.email],
                        fail_silently=False,
                    )

                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status='success',
                        server_response='OK',
                    )

                    self.stdout.write(
                        self.style.SUCCESS(f'Успешно отправлено для {recipient.email}')
                    )
                except Exception as e:
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status='failed',
                        server_response=str(e),
                    )

                    self.stdout.write(
                        self.style.ERROR(f'Ошибка для {recipient.email}: {str(e)}')
                    )
