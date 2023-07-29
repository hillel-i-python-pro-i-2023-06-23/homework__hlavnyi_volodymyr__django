from django.shortcuts import render

from apps.first_example.services.generate_humans_hw11 import generate_humans_hw11


def generate_humans_hw11_view(
    request,
    amount: int = 10,
):
    list_of_humans = generate_humans_hw11(amount=amount)
    # list_of_humans_checked = check_unique_human_hw11(list_of_humans)

    return render(
        request=request,
        template_name="first_example/generate_humans_hw11.html",
        context=dict(
            humans=list_of_humans,
        ),
    )
