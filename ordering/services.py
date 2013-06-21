from customers.services        import CustomerManager
from payment_gateways.services import PaymentMethodManager

from models import Order, Product, LineItem

from processes.order_to_cash_process import OrderToCashProcess

from common.distributed.distributed import compute_uuid

class OrderManager:

    customer_manager = CustomerManager()
    payment_method_manager = PaymentMethodManager()
    order_to_cash_process  = OrderToCashProcess()

    def create_order(self, params):

        email   = params.get('account',         None)
        pm_id   = params.get('payment_method',  None)
        events  = params.get('events',         None)

        if not email or not pm_id or not events:
            return None

        account = self.customer_manager.get_account(email)
        payment_method = self.payment_method_manager.get_valid_payment_method(pm_id, account)
        billing_address = self.customer_manager.get_billing_address(account)

        if not account or not payment_method:
            return None

        products = [self.get_product(event) for event in events]
        amount   = sum([product.price for product in products])

        subs = filter(None, [product.create_subscription(account, payment_method) for product in products])

        total = amount*1.20
        vat   = total - amount

        currency = 'GBP'
        country = 'ES'
        order_code = compute_uuid()

        order = Order(account=account, payment_method=payment_method, total=total, currency=currency, country=country, order_code=order_code, vat=vat, amount=amount)
        order.save()

        line_items = [self.create_line_item(product, event, order) for (event, product) in zip(events, products)]

        self.order_to_cash_process.start_online_order_to_cash_process(order, line_items, account, billing_address)

        return order

    def get_product(self, event):
        return Product.objects.get(code=event['rated_by_billing']['billing_code'])

    def create_line_item(self, product, event, order):
        quantity = event['rated_by_billing']['units'] + event['rated_by_billing']['units']/100

        line_item = LineItem(product=product, quantity=quantity, order=order)

        line_item.save()

        return line_item
