from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User

NAME = "users"


class Command(BaseCommand):

    help = "This Command creates many users"
    # print("hello")

    def add_arguments(self, parser):

        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many {} do you want to create?".format(NAME),
        )

    def handle(self, *args, **options):

        # times = int(options.get("times"))
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS("{} {} created!".format(number, NAME)))
        # self.stdout.write(self.style.WARNING("Warning message"))
        # self.stdout.write(self.style.ERROR("Error message"))
