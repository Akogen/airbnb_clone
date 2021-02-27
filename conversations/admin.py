from django.contrib import admin
from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ MessageAdmin Object Definition """

    list_display = (
        "__str__",
        "created",
    )


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ ConversationAdmin Object Definition """

    list_display = (
        "__str__",
        "count_messages",
        "count_participants",
    )
