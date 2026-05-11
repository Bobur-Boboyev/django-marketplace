def filter_products(queryset, params):

    category = params.get("category")
    price_min = params.get("price_min")
    price_max = params.get("price_max")
    search = params.get("search")

    if category:
        queryset = queryset.filter(
            category__slug=category
        )

    if price_min and price_max:
        queryset = queryset.filter(
            price__range=(price_min, price_max)
        )
    elif price_min:
        queryset = queryset.filter(price__gte=price_min)
    elif price_max:
        queryset = queryset.filter(price__lte=price_max)

    if search:
        queryset = queryset.filter(
            name__icontains=search
        )

    return queryset