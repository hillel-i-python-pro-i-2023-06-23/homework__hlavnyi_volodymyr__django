from django.http import HttpResponse


# Create your views here.
def home_page(request):
    # return render(request, 'index.html')
    return HttpResponse("Hello, world. You're at the home_page (base) index!")
