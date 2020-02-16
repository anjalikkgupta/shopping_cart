from .models import Order

def product_order_count(user):
	orders = Order.objects.filter(user=user, ordered=False)
	order = orders[0]
	if orders.exists():
		order_count = order.orderitems.count()
	else:
		order_count = None, 0
	return order_count