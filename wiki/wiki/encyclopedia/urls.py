from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.get_entry, name="entry"),
    path("search", views.search_results, name="search"),
    path("create", views.create, name="create"),
    path("build", views.build_page, name="build"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("random", views.random, name = "random")
]
