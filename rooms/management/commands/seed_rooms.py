import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


NAME = "rooms"


class Command(BaseCommand):

    hhelp = "This Command creates many {}".format(NAME)
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
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()

        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(100, 300),
                "guests": lambda x: random.randint(1, 20),
                "beds": lambda x: random.randint(2, 5),
                "bedrooms": lambda x: random.randint(2, 5),
                "bathrooms": lambda x: random.randint(2, 5),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))

        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)

            for i in range(3, random.randint(10, 31)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file="/room_photos/{}.webp".format(random.randint(1, 31)),
                )
            for amenity in amenities:
                random_number = random.randint(1, 30)
                if random_number % 2 == 0:
                    room.amenities.add(amenity)
            for facility in facilities:
                random_number = random.randint(1, 10)
                if random_number % 2 == 0:
                    room.facilities.add(facility)
            for house_rule in house_rules:
                random_number = random.randint(1, 10)
                if random_number % 2 == 0:
                    room.house_rules.add(house_rule)

        self.stdout.write(self.style.SUCCESS("{} {} created!".format(number, NAME)))
        # self.stdout.write(self.style.WARNING("Warning message"))
        # self.stdout.write(self.style.ERROR("Error message"))
