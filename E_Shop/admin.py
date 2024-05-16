from django.contrib import admin
from django.core.checks import Tags

# Register your models here.
from .models import *

class ImagesTublerinline(admin.TabularInline):
    model = Image

class TagsTublerinline(admin.TabularInline):
    model = Tag

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesTublerinline, TagsTublerinline]

class OrderItemTublerinline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTublerinline]
    list_display = ['firstname', 'phone', 'email', 'payment_id', 'paid', 'date']
    search_fields = ['firstname', 'email', 'payment_id']
    list_filter = ['date']


admin.site.register(Image)
admin.site.register(Tag)

admin.site.register(Categorie)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Filter_Price)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact_us)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
