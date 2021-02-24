from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"

    GENDER_CHOICES = ((GENDER_MALE, "Male"), (GENDER_FEMALE, "Female"))

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_KOREAN, "Korean"))

    CURRENCY_ENGLISH = "usd"
    CURRENCY_KOREAN = "krw"

    CURRENCY_CHOICES = ((CURRENCY_ENGLISH, "USD"), (CURRENCY_KOREAN, "KRW"))

    avatar = models.ImageField(blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=10,
        default=GENDER_MALE,
        blank=True,
    )
    bio = models.TextField(default="")
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True)
    super_hosts = models.BooleanField(default=False)
