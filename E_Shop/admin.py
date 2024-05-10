from django.contrib import admin
from django.core.checks import Tags

# Register your models here.
from .models import *

class ImagesTublerinline(admin.TabularInline):
    model = Images

class TagsTublerinline(admin.TabularInline):
    model = Tag

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesTublerinline, TagsTublerinline]

class OrderItemTublerinline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTublerinline]


admin.site.register(Images)
admin.site.register(Tag)

admin.site.register(Categoires)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Filter_Price)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact_us)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
