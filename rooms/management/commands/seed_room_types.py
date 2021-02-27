from django.core.management.base import BaseCommand
from rooms.models import RoomType


NAME = "room types"


class Command(BaseCommand):

    help = "This Command creates many {}".format(NAME)
    # print("hello")
    """
    def add_arguments(self, parser):

        parser.add_argument(
            "--times",
            help="How many times repeat?",
        )
    """

    def handle(self, *args, **options):
        room_types = [
            "Entire place",
            "Hotel room",
            "Private room",
            "Shared room",
        ]

        # times = int(options.get("times"))

        for room_type in room_types:
            RoomType.objects.create(name=room_type)

        self.stdout.write(self.style.SUCCESS("{} created!".format(NAME)))
        # self.stdout.write(self.style.WARNING("Warning message"))
        # self.stdout.write(self.style.ERROR("Error message"))
