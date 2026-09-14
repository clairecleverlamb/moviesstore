from django.urls import path
from . import manage_views, views

urlpatterns = [
    path('', views.index, name='cart.index'),
    path('manage/', manage_views.order_list, name='cart.manage_orders'),
    path('manage/create/', manage_views.order_create, name='cart.manage_order_create'),
    path('manage/<int:order_id>/edit/', manage_views.order_update, name='cart.manage_order_edit'),
    path('manage/<int:order_id>/delete/', manage_views.order_delete, name='cart.manage_order_delete'),
    path('<int:id>/add/', views.add_to_cart, name='cart.add'),
    path('clear/', views.clear, name='cart.clear'),
    path('purchase/', views.purchase, name='cart.purchase'),
]
