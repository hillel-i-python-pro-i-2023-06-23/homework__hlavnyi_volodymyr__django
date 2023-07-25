from django.shortcuts import render

from apps.first_example.services.generate_humans import generate_humans


def generate_humans_view(
    request,
    amount: int = 5,
):
    humans = generate_humans(amount=amount)

    return render(
        request=request,
        template_name="first_example/generate_humans.html",
        context=dict(
            humans=humans,
        ),
    )
