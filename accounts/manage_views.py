from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from cart.models import Order
from movies.models import Movie, Review, ReviewReport

from .decorators import staff_required
from .forms import StaffUserCreateForm, StaffUserUpdateForm


@staff_required
def dashboard(request):
    template_data = {
        'title': 'Manage Store',
        'user_count': User.objects.count(),
        'movie_count': Movie.objects.count(),
        'review_count': Review.objects.count(),
        'hidden_review_count': Review.objects.filter(is_hidden=True).count(),
        'report_count': ReviewReport.objects.count(),
        'order_count': Order.objects.count(),
    }
    return render(request, 'accounts/manage_dashboard.html',
                  {'template_data': template_data})


@staff_required
def user_list(request):
    users = User.objects.annotate(order_count=Count('order')).order_by('username')
    return render(request, 'accounts/manage_user_list.html', {
        'template_data': {
            'title': 'Manage Users',
            'users': users,
        },
    })


@staff_required
def user_create(request):
    form = StaffUserCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'User created.')
        return redirect('accounts.manage_users')
    return render(request, 'accounts/manage_user_form.html', {
        'template_data': {
            'title': 'Create User',
            'form': form,
            'submit_label': 'Create User',
        },
    })


@staff_required
def user_update(request, user_id):
    managed_user = get_object_or_404(User, id=user_id)
    form = StaffUserUpdateForm(request.POST or None, instance=managed_user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'User updated.')
        return redirect('accounts.manage_users')
    return render(request, 'accounts/manage_user_form.html', {
        'template_data': {
            'title': f'Edit {managed_user.username}',
            'form': form,
            'submit_label': 'Save User',
        },
    })


@staff_required
def user_delete(request, user_id):
    managed_user = get_object_or_404(User, id=user_id)
    if managed_user == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('accounts.manage_users')
    if request.method == 'POST':
        username = managed_user.username
        managed_user.delete()
        messages.success(request, f'User {username} deleted.')
        return redirect('accounts.manage_users')
    return render(request, 'accounts/manage_confirm_delete.html', {
        'template_data': {
            'title': 'Delete User',
            'object_label': f'user {managed_user.username}',
            'cancel_url': 'accounts.manage_users',
        },
    })
