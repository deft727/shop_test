from cart.cart import Cart


class MyMixin():
    def get_final_price(self):
        cart = Cart(self.request)
        total_bill = 0.0
        for key,value in self.request.session['cart'].items():
            total_bill = total_bill + (float(value['price']) * int(value['quantity']))
        return total_bill


