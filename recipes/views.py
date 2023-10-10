from django.shortcuts import render
# from django.http import HttpResponse


# Create your views here.


def home(request):
    return render(request, 'recipes/pages/home.html', status=200, context={
        'name': 'Maya Florentino',
    })


def recipes(request, id):
    return render(request, 'recipes/pages/home.html')
