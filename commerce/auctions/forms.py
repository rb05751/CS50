from django import forms
from .models import Listings

Categories = [('home', 'Home'), ('auto', 'Auto'),
              ('entertainment', 'Entertainment')]


class BidForm(forms.Form):
    amount = forms.IntegerField(label='Bid Amount')


class CommentForm(forms.Form):
    comment = forms.CharField(label='Add Comment', widget=forms.Textarea)


class ListingForm(forms.Form):
    title = forms.CharField(label="Title of Listing", max_length=100)
    price = forms.IntegerField(label="Price of Listing")
    description = forms.CharField(label="Listing Description")
    image_url = forms.CharField(
        label="Image Link", max_length=300)
    category = forms.CharField(
        label="Category", widget=forms.Select(choices=Categories))
