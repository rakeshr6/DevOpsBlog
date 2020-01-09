from django.shortcuts import render
from django.views.generic import CreateView

from .models import *


def index(request):
    topping = Topping.objects.all()
    pizza = Pizza.objects.all()
    context = {'topping': topping,
               'pizza': pizza
               }
    return render(request, 'testdemo/index.html', context)


# class CreateViewPage(CreateView):
#     model = Restaurant
#     template_name = 'testdemo/create.html'
#     fields = '__all__'