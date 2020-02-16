from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ModelForm


class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(default=0)
    product_image = models.ImageField(upload_to='images/', blank=True)
    description = models.CharField(max_length=500)
    price = models.FloatField()
    disc_price = models.FloatField()

    def __str__(self):
        return self.title


User = get_user_model()
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'

    def total_price(self):
        total = self.item.price * self.quantity
        floattotal = float("{0:.2f}".format(total))
        return floattotal

    def total_disc_price(self):
        total = self.item.disc_price * self.quantity
        floattotal = float("{0:.2f}".format(total))
        return floattotal


class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.total_price()
        return total


# class BillingAddress(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     address = models.CharField(max_length=100)
#     zipcode = models.CharField(max_length=50)
#     city = models.CharField(max_length=30)
#     landmark = models.CharField(max_length=20)
#
#     def __str__(self):
#         return f'{self.user.username} billing address'
#
#     class Meta:
#         verbose_name_plural = "Billing Addresses"
#
#
# class BillingForm(ModelForm):
#
#     class Meta:
#         model = BillingAddress
#         fields = ['address', 'zipcode', 'city', 'landmark']