from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewReportForm
from .models import Movie, Review, ReviewReport


def index(request):
    search_term = request.GET.get('search') ## retrive the values of the search
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie, is_hidden=False)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['report_form'] = ReviewReportForm()
    return render(request, 'movies/show.html',
                  {'template_data': template_data})


@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)


@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)


@login_required
def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, movie_id=id, is_hidden=False)
    if request.method != 'POST':
        return redirect('movies.show', id=id)
    if request.user == review.user:
        messages.error(request, 'You cannot report your own review.')
        return redirect('movies.show', id=id)
    if ReviewReport.objects.filter(review=review, user=request.user).exists():
        messages.info(request, 'You already reported this review.')
        return redirect('movies.show', id=id)

    form = ReviewReportForm(request.POST)
    if form.is_valid():
        ReviewReport.objects.create(
            review=review,
            user=request.user,
            reason=form.cleaned_data.get('reason', ''),
        )
        review.is_hidden = True
        review.save(update_fields=['is_hidden'])
        messages.success(request, 'Review reported and removed from this page.')
    return redirect('movies.show', id=id)