from .models import BluelineId


def send_order(order):
    kwargs = {
        'number': order.number,
        'incl': order.price_with_discount_without_deposit.incl,
        'excl': order.price_with_discount_without_deposit.excl,
        'deposit': order.total_deposit_incl_tax,
        'box_count': sum(order.lines.filter(
            product__has_box=True).values_list('quantity', flat=True)),
        'items_count': sum(order.lines.values_list('quantity', flat=True)),
        'date_placed': order.date_placed.timestamp(),
    }
    return BluelineId._send(**kwargs)
