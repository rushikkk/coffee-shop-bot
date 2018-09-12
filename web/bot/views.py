from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

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


def ajax_orders(request):
    if request.method == 'GET':
        orders = Orders.objects.order_by('-ordered_at')[0:15].values()
        context = {
            'orders': orders,
        }
        return render(request, 'bot/orders_ajax.html', context)

def orders2(request):
    orders_list = Orders.objects.order_by('-ordered_at').all()
    paginator = Paginator(orders_list, 15)  # Show 25 contacts per page

    page = request.GET.get('page')
    orders = paginator.get_page(page)
    return render(request, 'bot/orders2.html', {'orders': orders})