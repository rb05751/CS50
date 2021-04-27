from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listings(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image_url = models.CharField(max_length=300, default='www.google.com')
    category = models.CharField(max_length=100, default='Home')
    active = models.BooleanField(default=1)


class Winners(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, default=1)
    comment = models.TextField()


class WatchList(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Bids(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
