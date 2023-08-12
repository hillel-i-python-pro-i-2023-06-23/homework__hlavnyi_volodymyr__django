from django.http import HttpResponse
from django.views.generic import TemplateView


class GreetingsView(TemplateView):
    template_name = "first_example/greetings.html"

    def get_context_data(self, name: str, age: int, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            name=name,
            age=age,
            #
            title="Greetings",
        )

        return context


def greetings(request, name: str, age: int):
    return HttpResponse(f"Hi {name}. You are {age} years old.")


def greetings_simple_hi(request):
    return HttpResponse("Hi")
