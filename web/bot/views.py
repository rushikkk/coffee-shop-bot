from django.http import Http404
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse
from .models import Coffee, Orders


def index(request):
    coffee_list = Coffee.objects.all()
    context = {
        'coffee_list': coffee_list,
    }
    return render(request, 'bot/index.html', context)


def detail(request, coffee_id):
    coffee = get_object_or_404(Coffee, id=coffee_id)
    return render(request, 'bot/detail.html', {'coffee': coffee})


def results(request, question_id):
    response = "You're looking at the results of order %s."
    return HttpResponse(response % question_id)


def orders(request):
    orders = Orders.objects.order_by('-ordered_at')[0:15]
    context = {
        'orders': orders,
    }
    return render(request, 'bot/orders.html', context)