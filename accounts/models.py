from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    CATEGORY = (
        ("Indoor", "Indoor"),
        ("Out Door", "Out Door"),
    )
    name = models.CharField(max_length=255, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(
        max_length=255, null=True, choices=CATEGORY)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):

    STATUS = (
        ("Pending", "Pending"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
    )
    # customer =
    # product =

    created_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=255, null=True, choices=STATUS)
