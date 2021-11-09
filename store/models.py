from django.db import models

from users.models import Users

# Create your models here.
class Product(models.Model):

    author = models.CharField(default="",max_length=15),
    title = models.CharField(default="",max_length=30),
    image = models.ImageField(),
    base_price = models.IntegerField(),
    description = models.CharField(max_length=50)
    base_quantity = models.IntegerField(default=1)

class Wishlist(models.Model):

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Cart(models.Model):

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(models.Model):

    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    name = models.CharField(max_length=20)
    contact_number = models.IntegerField()
    pincode = models.IntegerField()
    locality = models.CharField(max_length=15,default="")
    address = models.CharField(max_length=50)
    city =models.CharField(max_length=20)
    landmark=models.CharField(max_length=20,default="")
    address_type = models.CharField(max_length=10,default="home")

class OrderItem(models.Model):

    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    probuct = models.ForeignKey(Product,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)


    