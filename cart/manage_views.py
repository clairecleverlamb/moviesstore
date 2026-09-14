from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import staff_required

from .forms import ItemFormSet, OrderForm
from .models import Order


def _save_order(order_form, item_formset):
    order = order_form.save(commit=False)
    if not order.pk:
        order.total = 0
        order.save()
    item_formset.instance = order
    item_formset.save()
    total = sum(item.price * item.quantity for item in order.item_set.all())
    order.total = total
    order.save()
    return order


@staff_required
def order_list(request):
    orders = Order.objects.select_related('user').order_by('-date')
    return render(request, 'cart/manage_order_list.html', {
        'template_data': {
            'title': 'Manage Orders',
            'orders': orders,
        },
    })


@staff_required
def order_create(request):
    order = Order()
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = ItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            _save_order(form, formset)
            messages.success(request, 'Order created.')
            return redirect('cart.manage_orders')
    else:
        form = OrderForm(instance=order)
        formset = ItemFormSet(instance=order)
    return render(request, 'cart/manage_order_form.html', {
        'template_data': {
            'title': 'Create Order',
            'form': form,
            'formset': formset,
            'submit_label': 'Create Order',
        },
    })


@staff_required
def order_update(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = ItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            _save_order(form, formset)
            messages.success(request, 'Order updated.')
            return redirect('cart.manage_orders')
    else:
        form = OrderForm(instance=order)
        formset = ItemFormSet(instance=order)
    return render(request, 'cart/manage_order_form.html', {
        'template_data': {
            'title': f'Edit Order #{order.id}',
            'form': form,
            'formset': formset,
            'submit_label': 'Save Order',
        },
    })


@staff_required
def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        messages.success(request, f'Order #{order_id} deleted.')
        return redirect('cart.manage_orders')
    return render(request, 'accounts/manage_confirm_delete.html', {
        'template_data': {
            'title': 'Delete Order',
            'object_label': f'order #{order.id}',
            'cancel_url': 'cart.manage_orders',
        },
    })
