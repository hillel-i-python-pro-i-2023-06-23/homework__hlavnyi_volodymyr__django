from django.views.generic import TemplateView


# def greetings(request, name: str, age: int):
#    return render(
#        request=request,
#        template_name="first_example/greetings.html",
#        context={
#            "name": name,
#            "age": age,
#            #
#            "title": "Greetings",
#        },
#    )


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


# def greetings(request, name: str, age: int):
#    return HttpResponse(f"Hi {name}. You are {age} years old.")


# def greetings_simple_hi(request):
#    return HttpResponse("Hi")


# def generate_users(request, amount: int = 50):
#    users = generate_list_of_users(amount=amount)
#    return HttpResponse(generate_string_list_of_users(users=users, type_of_list="ol"))
