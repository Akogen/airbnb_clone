from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models


class LoginView_scracth(View):

    """ LoginView Definition """

    def get(self, request):

        form = forms.LoginForm()

        return render(request, "users/login.html", {"form": form})

    def post(self, request):

        form = forms.LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = authenticate(username=email, password=password)

            if user is not None:

                # A backend authenticated the credential
                login(request, user)
                return redirect(reverse("core:home"))

        return render(request, "users/login.html", {"form": form})


class LoginView(FormView):

    """ LoginView Definition """

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    # initial = {"email": "email@email.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=email, password=password)

        if user is not None:

            # A backend authenticated the credential
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):

    logout(request)

    return redirect(reverse("core:home"))


class SignUpView(FormView):

    """ SignUp View Definition"""

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {"first_name": "David", "last_name": "Cool", "email": "email@email.com"}

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=email, password=password)

        if user is not None:

            # A backend authenticated the credential
            login(self.request, user)

        user.verify_email()

        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add succes message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))
