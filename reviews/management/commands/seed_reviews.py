import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from users import models as user_models
from rooms import models as room_models


NAME = "reviews"


class Command(BaseCommand):

    elp = "This Command creates many {}".format(NAME)
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
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder.add_entity(
            review_models.Review,
            number,
            {
                "accuracy": lambda x: random.randint(1, 6),
                "communication": lambda x: random.randint(1, 6),
                "cleanliness": lambda x: random.randint(1, 6),
                "location": lambda x: random.randint(1, 6),
                "check_in": lambda x: random.randint(1, 6),
                "value": lambda x: random.randint(1, 6),
                "room": lambda x: random.choice(rooms),
                "user": lambda x: random.choice(users),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS("{} {} created!".format(number, NAME)))
        # self.stdout.write(self.style.WARNING("Warning message"))
        # self.stdout.write(self.style.ERROR("Error message"))
