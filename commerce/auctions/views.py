from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django.db.models import FloatField
import bs4
from bs4 import BeautifulSoup as BS


from .models import User, Listings, WatchList, Bids, Winners, Comments
from .forms import BidForm, CommentForm, ListingForm


def index(request):
    try:
        user = User.objects.get(username=request.user.username)
        return render(request, "auctions/index.html", {
            "listings": Listings.objects.all(),
            "user": user
        })
    except:
        return render(request, "auctions/index.html", {
            "listings": Listings.objects.all(),
            "user": None
        })


def create(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        title = request.POST["title"]
        price = request.POST["price"]
        description = request.POST["description"]
        url = request.POST["image_url"]
        category = request.POST["category"]
        listing = Listings.objects.create(
            creator=user, title=title, price=price, description=description, image_url=url, category=category)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {
            "form": ListingForm()
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def is_in_watch(listing_id, user_id):
    if WatchList.objects.filter(listing=listing_id, user=user_id).exists():
        return True
    else:
        return False


def listing(request, listing_id):
    form = BidForm()  # What is this doing here?
    listing = Listings.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user.username)
    if user == listing.creator:
        is_user = True
    else:
        is_user = False
    value = is_in_watch(listing_id=listing_id, user_id=user.id)

    # Determine if there is a winner or not:
    bids = Bids.objects.filter(listing=listing).order_by('-amount')[0]
    winner_name = bids.user.username
    winner_amount = bids.amount
    winner = [winner_name, winner_amount]
    if len(winner) < 2:
        winner = False
    else:
        el_ganador = Winners.objects.create(user=user, listing=listing)
        el_ganador.save()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "value": value,
        "form": BidForm(),
        "is_user": is_user,
        "active": listing.active,
        "winner": winner[0],
        "bid": winner[1],
        "comment_form": CommentForm(),
        "comments": Comments.objects.all()
    })


def watch(request, id):
    user = User.objects.get(username=request.user.username)
    listing = Listings.objects.get(pk=id)
    new_item = WatchList.objects.create(listing=listing, user=user)
    new_item.save()
    return HttpResponseRedirect(reverse("index"))


def remove(request, id):
    user = User.objects.get(username=request.user.username)
    WatchList.objects.filter(listing=id, user=user.id).delete()
    return HttpResponseRedirect(reverse("index"))


def check_user(user_obj, listing_obj):
    if user_obj == listing_obj.creator:
        is_user = True
    else:
        is_user = False

    return is_user


def bid(request, id):
    user = User.objects.get(username=request.user.username)
    listing = Listings.objects.get(id=id)
    is_user = check_user(user_obj=user, listing_obj=listing)
    start_bid = listing.price
    all_listing_bids = Bids.objects.filter(listing=id).all()
    value = is_in_watch(listing_id=listing.id, user_id=user.id)

    if len(all_listing_bids) > 1:
        max_bid = int(Bids.objects.all().aggregate(
            max_bid=Max('amount', output_field=FloatField()))['max_bid'])
    else:
        max_bid = 0

    if request.method == "POST":
        bid_amount = int(request.POST["amount"])
        if ((bid_amount > start_bid) and (bid_amount > max_bid)):
            Bids.objects.create(listing=listing, amount=bid_amount, user=user)
            return render(request, "auctions/listing.html",
                          {
                              "listing": listing,
                              "value": value,
                              "form": BidForm(),
                              "is_user": is_user,
                              "active": listing.active,
                              "winner": False
                          })
        else:
            return render(request, "auctions/listing.html",
                          {
                              "listing": listing,
                              "value": value,
                              "form": BidForm(),
                              "is_user": is_user,
                              "active": listing.active,
                              "winner": False
                          })
    else:
        return render(request, "auctions/listing.html",
                      {
                          "listing": listing,
                          "value": value,
                          "form": BidForm(),
                          "is_user": is_user,
                          "active": listing.active,
                          "winner": False
                      })


def close_auction(request, id):
    # change listing to inactive when user closes auction
    listing = Listings.objects.get(pk=id)
    listing.active = False
    listing.save()

    return HttpResponseRedirect(reverse("listing", args=(id,)))


def reactivate(request, id):
    # change listing to inactive when user closes auction
    listing = Listings.objects.get(pk=id)
    listing.active = True
    listing.save()

    return HttpResponseRedirect(reverse("listing", args=(id,)))


def comment(request, id):
    user = User.objects.get(username=request.user.username)
    listing = Listings.objects.get(id=id)
    is_user = check_user(user_obj=user, listing_obj=listing)

    # process form:
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            new_comment = Comments.objects.create(
                user=user, listing=listing, comment=comment)
            new_comment.save()
            return HttpResponseRedirect(reverse("listing", args=(id,)))
        else:
            return HttpResponseRedirect(reverse("listing", args=(id,)))

    else:
        return Comments.objects.all()


def watch_list(request):
    user = User.objects.get(username=request.user.username)
    if WatchList.objects.filter(user=user).count() >= 1:
        watched_listings = []
        for item in WatchList.objects.filter(user=user):
            listing = Listings.objects.get(title=item.listing.title)
            watched_listings.append(listing)

        return render(request, "auctions/watchlist.html", {
            "watched_listings": watched_listings
        })
    else:
        return HttpResponseRedirect(reverse("index"))


def categories(request):
    return render(request, "auctions/categories.html", {
        "home": "home",
        "auto": "auto",
        "entertainment": "entertainment"
    })


def category_listings(request, category):
    listings = Listings.objects.filter(category=category.lower())
    return render(request, "auctions/view_categories.html", {
        "listings": listings
    })
