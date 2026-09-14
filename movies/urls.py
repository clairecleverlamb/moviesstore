from django.urls import path
from . import manage_views, views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('manage/', manage_views.movie_list, name='movies.manage_list'),
    path('manage/create/', manage_views.movie_create, name='movies.manage_create'),
    path('manage/<int:movie_id>/edit/', manage_views.movie_update, name='movies.manage_edit'),
    path('manage/<int:movie_id>/delete/', manage_views.movie_delete, name='movies.manage_delete'),
    path('manage/reviews/', manage_views.review_list, name='movies.manage_reviews'),
    path('manage/reviews/create/', manage_views.review_create, name='movies.manage_review_create'),
    path('manage/reviews/<int:review_id>/edit/', manage_views.review_update, name='movies.manage_review_edit'),
    path('manage/reviews/<int:review_id>/delete/', manage_views.review_delete, name='movies.manage_review_delete'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review,
        name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review,
        name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review,
        name='movies.delete_review'),
    path('<int:id>/review/<int:review_id>/report/', views.report_review,
        name='movies.report_review'),
]