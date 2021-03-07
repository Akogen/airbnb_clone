from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):

    model = models.Photo


# Antoher Option
class PhotoInline2(admin.StackedInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    inlines = (PhotoInline,)
    # inlines = (PhotoInline2,)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")},
        ),
        (
            "Spaces",
            {"fields": ("room_type", "guests", "beds", "bedrooms", "bathrooms")},
        ),
        (
            "Mores about the space",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        (
            "Last Details",
            {"fields": ("host",)},
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "bathrooms",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_facilities",
        "count_house_rules",
        "count_photos",
    )

    ordering = ("name", "price", "bedrooms")

    list_filter = (
        "instant_book",
        "host__super_hosts",
        "host__gender",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    search_fields = (
        "=city",
        "^host__username",
    )

    raw_id_fields = ("host",)

    filter_horizontal = ("facilities",)

    filter_vertical = ("house_rules",)

    # def save_model(self, request, obj, form, change):
    #    print(obj)
    #    super().save_model(self, request, obj, form, change)

    def count_amenities(self, obj):
        print(obj)
        return obj.amenities.count()

    count_amenities.short_description = "Amenities Count"

    def count_facilities(self, obj):
        return obj.facilities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    def count_house_rules(self, obj):
        return obj.house_rules.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe('<img src="{}"  width="50px" />'.format(obj.file.url))

    get_thumbnail.short_description = "Thumbnail"
