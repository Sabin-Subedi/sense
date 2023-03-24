from django.db import models
from helpers.models.base_model import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=256, verbose_name="Category Name")
    icon = models.ImageField(
        verbose_name="Category Icon",
    )


# Create your models here.
class Product(BaseModel):
    name = models.CharField(max_length=256, verbose_name="Product Name")
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    stock_qty = models.PositiveIntegerField(default=0, verbose_name="Stock Quantity")
    parent = models.ManyToManyField("self", symmetrical=False, through="")


class ProductFields(models.Model):
    Product
