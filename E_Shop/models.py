import uuid
from django.db import models
from django.utils import timezone
class Categoires(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Filter_Price(models.Model):
    FILTER_PRICE = (
        ('0 TO 200', '0 TO 200'),
        ('200 TO 500', '200 TO 500'),
        ('500 TO 1000', '500 TO 1000'),
        ('1000 TO 2000', '1000 TO 2000'),
        ('2000+', '2000+'),
    )
    price = models.CharField(choices=FILTER_PRICE, max_length=60)

    def __str__(self):
        return self.price

class Product(models.Model):
    CONDITION = (('New', 'New'), ('Old','Old'))
    STOCK = ('IN STOCK', 'IN STOCK'), ('OUT OF STOCK', 'OUT OF STOCK')
    STATUS = ('Publish', 'Publish'), ('Draft', 'Draft')

    unique_id = models.CharField(unique=True, max_length=200, null=False, blank=True)
    image = models.ImageField(upload_to='Product_images/img')
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    condition = models.CharField(choices=CONDITION, max_length=100)
    information = models.TextField()
    description = models.TextField()
    stock = models.CharField(choices=STOCK, max_length=200)
    status = models.CharField(choices=STATUS, max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    categories = models.ForeignKey(Categoires, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Filter_Price, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):

        if not self.unique_id:
            self.unique_id = str(uuid.uuid4().hex)[:10] + self.created_date.strftime('%Y%m%d')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Images(models.Model):
    image = models.ImageField(upload_to='Product_images/img')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

class Tag(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
