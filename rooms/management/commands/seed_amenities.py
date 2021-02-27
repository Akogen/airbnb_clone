from django.core.management.base import BaseCommand
from rooms.models import Amenity


NAME = "amenities"


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
        amenities = [
            "Air Conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boating",
            "Cable TV",
            "Carbon Monoxide Detectors",
            "Chairs",
            "Children Area",
            "Coffee Maker in Room",
            "Cooking Hob",
            "Cookware & Kitchen Utensils",
            "Dishwasher",
            "Double Bed",
            "En Suite Bathroom",
            "Free Parking",
            "Free Wireless Internet",
            "Freezer",
            "Fridge / Freezer",
            "Golf",
            "Hair Dryer",
            "Heating",
            "Hot Tub",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Outdoor Tennis",
            "Oven" "Queen Size Bed",
            "Restaurant",
            "Shopping Mall",
            "Shower",
            "Smoke Detectors",
            "Sofa",
            "Stereo",
            "Swimming Pool",
            "Toilet",
            "Towels",
            "Television",
        ]

        # times = int(options.get("times"))

        for amenity in amenities:
            Amenity.objects.create(name=amenity)

        self.stdout.write(self.style.SUCCESS("{} created!".format(NAME)))
        # self.stdout.write(self.style.WARNING("Warning message"))
        # self.stdout.write(self.style.ERROR("Error message"))
