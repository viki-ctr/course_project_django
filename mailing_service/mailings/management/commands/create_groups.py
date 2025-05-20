from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create manager group'

    def handle(self, *args, **options):
        managers, created = Group.objects.get_or_create(name='Менеджеры')
        permissions = Permission.objects.filter(
            codename__in=[
                'can_view_all_mailings',
                'can_edit_any_mailing',
                'can_disable_mailing',
                'can_view_all_messages',
                'can_edit_any_message',
                'can_view_all_recipients',
                'can_edit_any_recipient',
            ]
        )
        managers.permissions.set(permissions)
        self.stdout.write(
            self.style.SUCCESS('Группа "Менеджеры" успешно создана с необходимыми правами')
        )
