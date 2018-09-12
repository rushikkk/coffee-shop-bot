from django.urls import path

from . import views

urlpatterns = [
    # ex: /bot/
    path('', views.index, name='index'),
    # ex: /bot/5/
    path('<int:coffee_id>/', views.detail, name='detail'),
    # ex: /bot/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /bot/5/vote/
    path('orders/', views.orders, name='orders'),
    path('ajax/orders/', views.ajax_orders, name='ajax_orders'),
    path('orders2/', views.orders2, name='orders2'),
]