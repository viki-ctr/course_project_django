from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create manager group'

    def handle(self, *args, **options):
        managers, created = Group.objects.get_or_create(name='Менеджеры')
        permissions = Permission.objects.filter(
            codename__in=['view_mailing', 'view_recipient', 'view_message']
        )
        managers.permissions.set(permissions)
        self.stdout.write('Группа "Менеджеры" создана')
