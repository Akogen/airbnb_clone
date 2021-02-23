from django.contrib import admin
from . import models


@admin.register(models.Reservation)
class ReservationAmdin(admin.ModelAdmin):

    """ Reservation Admin Definition """

    pass