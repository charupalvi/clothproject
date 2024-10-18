from django.contrib import admin
from clothapp.models import Cloth,Cart,Order,Multiimage

# Register your models here.
class Clothadmin(admin.ModelAdmin):
    list_display=['name','category','brand','price','quantity','size','details','imagepath']
    list_filter=['category','price','brand']

class CartAdmin(admin.ModelAdmin):
    list_display=['id','clothid','uid','quantity']

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','orderid','userid','clothid','quantity']
    list_filter=['userid','clothid']

class MultiimageAdmin(admin.ModelAdmin):
    list_display=['id','clothid','imagepath']

admin.site.register(Cloth,Clothadmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Multiimage,MultiimageAdmin)