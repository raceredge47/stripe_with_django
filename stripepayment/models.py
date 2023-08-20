from django.db import models
from django.core import validators

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.FloatField(validators=[
            validators.MinValueValidator(0),
            validators.MaxValueValidator(100000)
        ])
    def __str__(self):
        return self.name


class OrderDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(to=Product, verbose_name='Product',
                                on_delete=models.PROTECT
                                )
    amount = models.IntegerField(verbose_name='Amount')
    stripe_payment_intent = models.CharField(max_length=200)
    has_paid = models.BooleanField(default=False, verbose_name='Payment Status')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)