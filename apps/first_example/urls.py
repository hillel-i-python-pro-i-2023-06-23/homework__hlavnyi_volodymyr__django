from django.urls import path
from . import views

app_name = "first_example"

urlpatterns = [
    path("", views.greetings_simple_hi, name="greetings_simple_hi"),
    path("hi/<name>/<int:age>/", views.greetings, name="greetings"),
    path("generate-users/", views.generate_users, name="generate_users"),
    path("generate-users/<int:amount>/", views.generate_users, name="generate_users"),
]
