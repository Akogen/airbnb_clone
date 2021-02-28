from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse  # for sample2 only
from . import models

# without render sample
def sample2(request):
    now = datetime.now()
    return HttpResponse(content="<h1>Hello {}</h1>".format(now))


# with render sample
def sample(request):
    now = datetime.now()
    hungry = True
    return render(request, "sample.html", context={"now": now, "hungry": hungry})


def home(request):
    all_rooms = models.Room.objects.all()
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
        },
    )
