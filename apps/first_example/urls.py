from django.urls import path, include
from . import views

app_name = "first_example"

urlpatterns = [
    path("hi/<name>/<int:age>/", views.GreetingsView.as_view(), name="greetings"),
    path(
        "generate-humans/",
        include(
            [
                path("<int:amount>/", views.generate_humans_view, name="generate_humans_with_amount"),
                path("", views.generate_humans_view, name="generate_humans"),
            ]
        ),
    ),
    path(
        "generate-humans-hw11/",
        include(
            [
                path("<int:amount>/", views.generate_humans_hw11_view, name="generate_humans_with_amount_hw11"),
                path("", views.generate_humans_hw11_view, name="generate_humans_hw11"),
            ]
        ),
    ),
]
