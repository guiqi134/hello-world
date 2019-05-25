from django.contrib import admin
from catalog.models import Account, Customer, Rider, Restaurant, Order, Food

# Register your models here.
# Register the Admin classes for Account using the decorator
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    pass

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    pass


