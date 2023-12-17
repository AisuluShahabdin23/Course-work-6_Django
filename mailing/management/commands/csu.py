from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='aisulu_sh_98@mail.ru',
            first_name='Admin',
            last_name='Adminka',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password('123qwe456rty')
        user.save()
