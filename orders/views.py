from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm
from django.db.models import Q

def order_list(request):
    categories = request.GET.getlist('categories')
    days_to_complete = request.GET.get('days_to_complete')
    price_min = request.GET.get('price_min', 0)
    price_max = request.GET.get('price_max', 1000000)
    negotiable = request.GET.get('negotiable') == 'on'
    search = request.GET.get('search', '')

    orders = Order.objects.all().order_by('-created_at')

    if categories:
        orders = orders.filter(category__in=categories)

    if days_to_complete:
        orders = orders.filter(days_to_complete__lte=days_to_complete)

    try:
        price_min = int(price_min)
        price_max = int(price_max)
    except (ValueError, TypeError):
        price_min = 0
        price_max = 1000000

    if negotiable:
        orders = orders.filter(is_budget_negotiable=True)
    else:
        budget_query = Q(is_budget_negotiable=True)
        
        non_negotiable_query = Q(is_budget_negotiable=False)
        if price_min > 0:
            non_negotiable_query &= Q(budget__gte=price_min)
        if price_max < 1000000:
            non_negotiable_query &= Q(budget__lte=price_max)
        
        budget_query |= non_negotiable_query
        orders = orders.filter(budget_query)

    if search:
        orders = orders.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )

    return render(request, 'orders/orders.html', {
        'orders': orders,
        'selected_categories': request.GET.getlist('categories'),
        'request.GET': request.GET,
    })

def order_view(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/orders.html', {'orders': orders})

@login_required
def create_order_view(request):
    if not request.user.is_customer:
        return redirect('orders')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer
            order.save()
            return redirect('orders') 
    else:
        form = OrderForm()
    
    return render(request, 'orders/create_order.html', {'form': form})