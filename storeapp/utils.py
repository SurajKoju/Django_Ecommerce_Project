import json
from . models import *

def cookieCart(request):
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart={}
        print('cart:', cart)
        items = []
        # to eliminate the error refresh we add this code
        order = {'get_cart_total': 0, 'get_cart_items':0, 'shipping': False}
        cartItems = order['get_cart_items']

        for i in cart:
            try:
                cartItems += cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = (product.price * cart[i]["quantity"])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]["quantity"]

                item={
                    'product':{
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                        },
                    'quantity': cart[i]["quantity"],
                    'get_total': total
                }
                items.append(item)

                if product.digital == False:
                    order['shipping'] = True
            except:
                pass

        return{'cartItems':cartItems, 'order': order, 'items': items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)#you can add complete = True or False
        # it gets all the ordered item.
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items


    else:
        cookieData= cookieCart(request)
        cartItems = cookieData['cartItems']
        order =cookieData['order']
        items =cookieData['items']

    return{'cartItems':cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    print("User isnot logged in...")
    print('cookies', request.COOKIES)

# offline user information records storingg in datavase
    name=data['form']['name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )
    print('..............')
    return customer, order