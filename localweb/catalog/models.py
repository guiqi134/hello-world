from django.db import models
import uuid
from catalog.choices import * 
from django.urls import reverse

# Create your models here.


class Account(models.Model):
    # regex_AName = r'^[a-z0-9_-]{3,16}$'
    # AName_validator = RegexValidator(regex=regex_AName, message='用户名非法输入')
    
    AName = models.CharField(primary_key=True, max_length=128)
    password = models.CharField(max_length=256)
    sex = models.CharField(max_length=32, choices=gender, default='male')
    last_name = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32)
    birth = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=True)
    personal_ID = models.CharField(max_length=18, unique=True)
    account_type = models.CharField(max_length=32, choices=account_types, default='customer')
    c_time = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-c_time']

    def __str__(self):
        return self.AName


class Customer(models.Model):
    AName = models.OneToOneField(
        Account, 
        primary_key=True, 
        on_delete=models.CASCADE,
        limit_choices_to={'account_type': 'customer'}
    )
    address = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['AName']

    def __str__(self):
        return '{0}({1})'.format(self.AName, self.address)


class Restaurant(models.Model):
    AName = models.OneToOneField(
        Account, 
        primary_key=True, 
        on_delete=models.CASCADE,
        limit_choices_to={'account_type': 'restaurant'}
    )
    RName = models.CharField(max_length=128, unique=True, blank=True, null=True)
    RImage = models.ImageField(upload_to='restaurant_image', blank=True, null=True)
    RType = models.CharField(max_length=32, choices=rest_types, blank=True, null=True)

    class Meta:
        ordering = ['RName']

    def __str__(self):
        return '{0}({1})'.format(self.RName, self.RType)

    def get_absolute_url(self):
        return reverse('restaurant-detail', args=[self.AName])


class Rider(models.Model):
    AName = models.OneToOneField(
        Account, 
        primary_key=True, 
        on_delete=models.CASCADE,
        limit_choices_to={'account_type': 'rider'}
    )
    fee = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['AName']

    def __str__(self):
        return '{0}({1})'.format(self.AName, self.fee)


class Food(models.Model):
    food_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    FName = models.CharField(max_length=128)
    RName = models.ForeignKey(Restaurant, on_delete=models.CASCADE, to_field='RName')
    price = models.FloatField(max_length=1000)
    count = models.IntegerField()
    FImage = models.ImageField(upload_to='food_image', blank=True)

    class Meta:
        ordering = ['FName', 'count']
        unique_together = ('FName', 'RName', 'price')

    def __str__(self):
        return '{0}({1})'.format(self.FName, self.RName)

    def get_absolute_url_add(self):
        return reverse('additem', args=[self.food_id])

    def get_absolute_url_delete(self):
        return reverse('removeitem', args=[self.food_id])


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    foods = models.ManyToManyField(Food)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    start_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(max_length=100, blank=True, null=True)
    order_status = models.IntegerField(choices=status, default=-1)
    rest_rating = models.FloatField(max_length=100, default=-1)
    rider_rating = models.FloatField(max_length=100, default=-1)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return '{0}({1}, {2}, {3}, {4})'.format(self.order_id, self.customer, self.restaurant, self.rider, self.order_status)

    # 1. foods must be link with the Food in that restaurant
    # 2. a customer/rest/rider only can have an account 
