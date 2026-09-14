from django.urls import path

from . import manage_views, views

urlpatterns = [
    path('signup/', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),
    path('manage/', manage_views.dashboard, name='accounts.manage'),
    path('manage/users/', manage_views.user_list, name='accounts.manage_users'),
    path('manage/users/create/', manage_views.user_create, name='accounts.manage_user_create'),
    path('manage/users/<int:user_id>/edit/', manage_views.user_update, name='accounts.manage_user_edit'),
    path('manage/users/<int:user_id>/delete/', manage_views.user_delete, name='accounts.manage_user_delete'),
]