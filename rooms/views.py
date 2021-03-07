from datetime import datetime
from math import ceil
from django.utils import timezone
from django.http import Http404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect
from django.http import HttpResponse  # for sample2 only
from django.core.paginator import Paginator, EmptyPage
from django_countries import countries
from . import models, forms


# without render sample
def listview_simple(request):
    now = datetime.now()
    return HttpResponse(content="<h1>Hello {}</h1>".format(now))


# with render sample
def listview_simple2(request):
    now = datetime.now()
    hungry = True
    return render(
        request, "rooms/listview_simple.html", context={"now": now, "hungry": hungry}
    )


def detailview_simple(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/room_detail.html", context={"room": room})
    except models.Room.DoesNotExist:
        # return redirect(reverse("core:home"))
        raise Http404()


# list Simple Format
def listview_simple3(request):
    # Lazy Loading
    all_rooms = models.Room.objects.all()[0:20]
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
        },
    )


# list from scratch
def listview_scratch(request):
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


# list from pagenator FBV get_page -- Less Control, everything ready to use
def listview_FBV_getpage(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()

    paginator = Paginator(room_list, 10, orphans=5)
    rooms = paginator.get_page(page)

    # print(vars(rooms.paginator))
    return render(request, "rooms/home_FBV_getpage.html", {"page": rooms})


# list from pagenator FBV page -- More Control, More Error ControlS
def listview_FBV_page(request):
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


class RoomDetail(DetailView):

    """ RoomDetaill Definition """

    model = models.Room


def search_scracth(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "US")
    # request.GET.get("room_type", 0) IS STRING
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    bathrooms = int(request.GET.get("bathrooms", 0))
    instant_book = bool(request.GET.get("instant_book", False))
    super_host = bool(request.GET.get("super_host", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {
        "selected_city": city,
        "selected_country": country,
        "selected_room_type": room_type,
        "selected_price": price,
        "selected_guests": guests,
        "selected_bedrooms": bedrooms,
        "selected_beds": beds,
        "selected_bathrooms": bathrooms,
        "selected_amenities": s_amenities,
        "selected_facilities": s_facilities,
        "selected_instant_book": instant_book,
        "selected_super_host": super_host,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk__exact"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if bathrooms != 0:
        filter_args["bathrooms__gte"] = bathrooms

    if instant_book is True:
        filter_args["instant_book"] = True

    if super_host is True:
        filter_args["host__super_host"] = True

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = models.Room.objects.filter(**filter_args)

    return render(
        request,
        "rooms/search_scratch.html",
        context={**form, **choices, "rooms": rooms},  # ** unpack
    )


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):

        form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


def search(request):

    country = request.GET.get("country")

    if country:

        form = forms.SearchForm(request.GET)

        if form.is_valid():
            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            bathrooms = form.cleaned_data.get("bathrooms")
            instant_book = form.cleaned_data.get("instant_book")
            super_host = form.cleaned_data.get("super_host")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            filter_args = {}

            if city != "Anywhere":
                filter_args["city__startswith"] = city

            filter_args["country"] = country

            if room_type is not None:
                filter_args["room_type"] = room_type

            if price is not None:
                filter_args["price__lte"] = price

            if guests is not None:
                filter_args["guests__gte"] = guests

            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms

            if beds is not None:
                filter_args["beds__gte"] = beds

            if bathrooms is not None:
                filter_args["bathrooms__gte"] = bathrooms

            if instant_book is True:
                filter_args["instant_book"] = True

            if super_host is True:
                print(super_host)
                filter_args["host__super_hosts"] = True

            for amenity in amenities:
                filter_args["amenities"] = amenity

            for facility in facilities:
                filter_args["facilities"] = facility

            qs = models.Room.objects.filter(**filter_args).order_by(
                "-created"
            )  # order by를 넣어야 순서가 정해지므로 Paginator에 문제가 안생긴다.
            # qs = models.Room.order_by("created") ???

            paginator = Paginator(qs, 10, orphans=5)

            page = request.GET.get("page", 1)

            rooms = paginator.get_page(page)

            return render(request, "rooms/search.html", {"form": form, "rooms": rooms})
    else:

        form = forms.SearchForm()

    return render(request, "rooms/search.html", {"form": form})  # 한칸위로 올린 이유 중요
