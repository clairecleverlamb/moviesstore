from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import staff_required

from .forms import MovieForm, StaffReviewForm
from .models import Movie, Review


@staff_required
def movie_list(request):
    return render(request, 'movies/manage_movie_list.html', {
        'template_data': {
            'title': 'Manage Movies',
            'movies': Movie.objects.order_by('name'),
        },
    })


@staff_required
def movie_create(request):
    form = MovieForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Movie created.')
        return redirect('movies.manage_list')
    return render(request, 'movies/manage_movie_form.html', {
        'template_data': {
            'title': 'Create Movie',
            'form': form,
            'submit_label': 'Create Movie',
        },
    })


@staff_required
def movie_update(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    form = MovieForm(request.POST or None, request.FILES or None, instance=movie)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Movie updated.')
        return redirect('movies.manage_list')
    return render(request, 'movies/manage_movie_form.html', {
        'template_data': {
            'title': f'Edit {movie.name}',
            'form': form,
            'submit_label': 'Save Movie',
        },
    })


@staff_required
def movie_delete(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        name = movie.name
        movie.delete()
        messages.success(request, f'Movie {name} deleted.')
        return redirect('movies.manage_list')
    return render(request, 'accounts/manage_confirm_delete.html', {
        'template_data': {
            'title': 'Delete Movie',
            'object_label': f'movie {movie.name}',
            'cancel_url': 'movies.manage_list',
        },
    })


@staff_required
def review_list(request):
    reviews = Review.objects.select_related('movie', 'user').prefetch_related('reports').order_by('-date')
    return render(request, 'movies/manage_review_list.html', {
        'template_data': {
            'title': 'Manage Reviews',
            'reviews': reviews,
        },
    })


@staff_required
def review_create(request):
    form = StaffReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Review created.')
        return redirect('movies.manage_reviews')
    return render(request, 'movies/manage_review_form.html', {
        'template_data': {
            'title': 'Create Review',
            'form': form,
            'submit_label': 'Create Review',
        },
    })


@staff_required
def review_update(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    form = StaffReviewForm(request.POST or None, instance=review)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Review updated.')
        return redirect('movies.manage_reviews')
    return render(request, 'movies/manage_review_form.html', {
        'template_data': {
            'title': 'Edit Review',
            'form': form,
            'submit_label': 'Save Review',
        },
    })


@staff_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted.')
        return redirect('movies.manage_reviews')
    return render(request, 'accounts/manage_confirm_delete.html', {
        'template_data': {
            'title': 'Delete Review',
            'object_label': f'review #{review.id}',
            'cancel_url': 'movies.manage_reviews',
        },
    })
