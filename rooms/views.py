from datetime import datetime
from math import ceil
from django.utils import timezone
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.http import HttpResponse  # for sample2 only
from django.core.paginator import Paginator, EmptyPage
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


# all_room Simple Format
def all_rooms_simple(request):
    # Lazy Loading
    all_rooms = models.Room.objects.all()[0:20]
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
        },
    )


# all_rooms from scratch
def all_rooms_scratch(request):
    # http://127.0.0.1:8000/?page=1&city=fullerton
    # Output: <QueryDict: {'page': ['1'], 'city': ['fullerton']}>
    # print(request.GET)  # "GET /?page=1&city=fullerton HTTP/1.1"
    # print(request.GET.get("page", 1))  # 1 default: 1
    # print(request.GET.get("city", 0))  # Fullerton   default: 0

    page = request.GET.get("page", 1)
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    page_count = models.Room.objects.count() / page_size
    page_range = range(1, ceil(page_count))

    all_rooms = models.Room.objects.all()[offset:limit]
    return render(
        request,
        "rooms/home_scratch.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": ceil(page_count),
            "page_range": page_range,
        },
    )


# all_rooms from pagenator FBV get_page -- Less Control, everything ready to use
def all_rooms_FBV_getpage(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()

    paginator = Paginator(room_list, 10, orphans=5)
    rooms = paginator.get_page(page)

    # print(vars(rooms.paginator))
    return render(request, "rooms/home_FBV_getpage.html", {"page": rooms})


# all_rooms from pagenator FBV page -- More Control, More Error ControlS
def all_rooms_FBV_page(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()

    paginator = Paginator(room_list, 10, orphans=5)

    try:
        rooms = paginator.page(int(page))
        # print(vars(rooms.paginator))
        return render(request, "rooms/home_FBV_page.html", {"page": rooms})
    except EmptyPage:
        return redirect("/")


# ccvb.co.uk
class HomeView(ListView):

    """ HomeVIew Definition """

    model = models.Room
    paginate_by = 10
    ordering = "created"
    paginate_orphans = 5
    page_kwarg = "page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context