from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


def can_change_status(user, order, new_status):

    if user.is_staff:
        return True

    vendor = getattr(user, "vendor", None)

    if order.user == user:
        return new_status == "cancelled" and order.status == "pending"

    if vendor and order.items.filter(product__vendor=vendor).exists():
        if order.status == "pending" and new_status in ["confirmed", "cancelled"]:
            return True

        if order.status == "confirmed" and new_status == "shipped":
            return True

    return False
