from django.contrib import admin
from .models import BuyerProfile , SellerProfile , Product , Cart
# Register your models here.
admin.site.register(BuyerProfile)

admin.site.register(SellerProfile)

admin.site.register(Product)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','item_quantity','item_amount']