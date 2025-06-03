from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='bip_bel@mail.ru',
            username='bipbel',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('yR@wd%qt')
        user.save()
