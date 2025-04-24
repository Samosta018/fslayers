from django.shortcuts import render
from django.db.models import Q
from users.models import Order

def index(request):
    orders = Order.objects.all().order_by('-created_at')
    search_query = request.GET.get('search', '')
    selected_categories = request.GET.getlist('category')
    max_days = request.GET.get('days')
    negotiable = request.GET.get('negotiable') == 'on'
    
    try:
        price_min = int(request.GET.get('priceMin', '0').replace(' ', ''))
    except (ValueError, AttributeError):
        price_min = 0
        
    try:
        price_max = int(request.GET.get('priceMax', '1000000').replace(' ', ''))
    except (ValueError, AttributeError):
        price_max = 1000000

    if search_query:
        orders = orders.filter(title__icontains=search_query)
    
    if selected_categories:
        orders = orders.filter(category__in=selected_categories)
    
    if max_days:
        try:
            orders = orders.filter(deadline__lte=int(max_days))
        except ValueError:
            pass

    price_filter = Q()
    if negotiable:
        price_filter |= Q(is_negotiable=True)
    if price_min > 0 or price_max < 1000000:
        price_filter |= Q(
            budget__gte=price_min,
            budget__lte=price_max,
            is_negotiable=False
        )
    
    orders = orders.filter(price_filter)

    context = {
        'orders': orders,
        'category_choices': Order.CATEGORY_CHOICES,
        'selected_categories': selected_categories,
        'search_query': search_query,
        'max_days': max_days,
        'negotiable': negotiable,
        'price_min': price_min,
        'price_max': price_max,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'partials/_orders_list.html', context)
    
    return render(request, 'pages/index.html', context)