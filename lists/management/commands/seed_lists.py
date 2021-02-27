import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models


NAME = "lists"


class Command(BaseCommand):

    help = "This Command creates many {}".format(NAME)
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
        # rooms = room_models.Room.objects.all()[4:10]
        seeder.add_entity(
            list_models.List,
            number,
            {
                "user": lambda x: random.choice(users),
            },
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS("{} {} created!".format(number, NAME)))
        # self.stdout.write(self.style.WARNING("Warning message"))
        # self.stdout.write(self.style.ERROR("Error message"))
