from django.core.management.base import BaseCommand
from rooms.models import Facility


NAME = "facilitiess"


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
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]

        # times = int(options.get("times"))

        for facility in facilities:
            Facility.objects.create(name=facility)

        self.stdout.write(self.style.SUCCESS("{} created!".format(NAME)))
        # self.stdout.write(self.style.WARNING("Warning message"))
        # self.stdout.write(self.style.ERROR("Error message"))
