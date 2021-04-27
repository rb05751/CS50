from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("watch/<int:id>", views.watch, name="watch"),
    path("remove/<int:id>", views.remove, name="remove"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("close/<int:id>", views.close_auction, name="close"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("reactivate/<int:id>", views.reactivate, name="reactivate"),
    path("watchlist", views.watch_list, name="watch_list"),
    path("categories", views.categories, name="categories"),
    path("category_listings/<str:category>",
         views.category_listings, name="category_listings")
]
