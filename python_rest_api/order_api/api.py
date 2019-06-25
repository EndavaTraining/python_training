from order_api.service import OrderService

class OrderApi:
    def __init__(self, context):
        self.context = context

    def list(self):
        return [order.to_json() for order in OrderService().list()]

    def add(self):
        order = from_json(self.context['body'])
        print(f'Saving order {order}')
        return OrderService().add(make_order(**order))

    def order_created(self):
        order = self.context['order']
        print(f'Order created {order}')
        order = make_order(**order)
        order.status = 'COMPLETED'
        OrderService().add(order)