from django.db import models
from django.contrib.auth.models import User

# customer model
class Customer(models.Model):
    # oneto one relation is for the user can be only one customer and customer can only have one user.
    user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)


    # from the below function the user data are shown in admin panel.
    def __str__(self):
        return self.name


# about  Products
class Product(models.Model):
    name = models.CharField(max_length = 200, null = True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(null = True, blank = True)
    # to set product image
    image = models.ImageField(null = True, blank = True)

    def __str__(self):
        return self.name

    # to handle image errors
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url




class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
    # models.DateTimeField properties might be different
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length = 100, null = True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True

        return shipping



    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    # to find how many items in the cart
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null = True)
    quantity = models.IntegerField(default = 0, null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add = True)

    # to get total amount when we add the items in cart
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank = True, null = True)
    address = models.CharField(max_length = 200, null = True)
    city = models.CharField(max_length = 200, null = True)
    state = models.CharField(max_length = 200, null = True)
    zipcode = models.CharField(max_length = 200, null = True)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.address
