from django.http import HttpResponse
from apps.first_example.generate_users import generate_list_of_users, generate_string_list_of_users


# Create your views here.
def greetings(request, name: str, age: int):
    return HttpResponse(f"Hi {name}. You are {age} years old.")


def greetings_simple_hi(request):
    return HttpResponse("Hi")


def generate_users(request, amount: int = 50):
    users = generate_list_of_users(amount=amount)
    return HttpResponse(generate_string_list_of_users(users=users, type_of_list="ol"))
