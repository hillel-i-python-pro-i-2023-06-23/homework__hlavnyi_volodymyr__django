import datetime
import random

from django.shortcuts import render


def some_func():
    return "debug123"


def home_page(request):
    now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")

    return render(
        request=request,
        template_name="base/home_page.html",
        context={
            "greetings_text": f"Hello, World! Now is {now} in UTC.",
            "nested": {
                "random_number": random.randint(1, 100),
            },
            "title": "Home page",
            "debug": some_func,
        },
    )
