import os
import requests
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


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"

    return redirect(
        "https://github.com/login/oauth/authorize?client_id={}&redirect_uri={}&scope=read:user".format(
            client_id, redirect_uri
        )
    )


class GithubException(Exception):

    """ GithubExcepton Definition """

    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)

        if code is not None:
            token_request = requests.post(
                "https://github.com/login/oauth/access_token?client_id={}&client_secret={}&code={}".format(
                    client_id, client_secret, code
                ),
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()

            error = token_json.get("error", None)

            if error is not None:
                raise GithubException()

            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": "token {}".format(access_token),
                        "Accept": "application/json",
                    },
                )

                profile_json = profile_request.json()

                username = profile_json.get("login", None)

                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")

                    try:
                        user = models.User.objects.get(email=email)

                        if user.login_method == models.User.LOGIN_GITHUB:
                            login(request, user)

                        else:
                            raise GithubException()

                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                        )

                        user.set_unusable_password()

                        user.save()

                    login(request, user)

                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()

        else:
            raise GithubException()
    except GithubException:
        # send error GithubException
        return redirect(reverse("users:login"))
