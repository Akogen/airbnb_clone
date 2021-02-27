from django.core.management.base import BaseCommand
from rooms.models import HouseRule


NAME = "house rules"


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
        house_rules = [
            "No Smoking",
            "No Pets",
            "No parties or events",
        ]

        # times = int(options.get("times"))

        for house_rule in house_rules:
            HouseRule.objects.create(name=house_rule)

        self.stdout.write(self.style.SUCCESS("{} created!".format(NAME)))
        # self.stdout.write(self.style.WARNING("Warning message"))
        # self.stdout.write(self.style.ERROR("Error message"))
