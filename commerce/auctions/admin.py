from django.contrib import admin
from .models import User, Listings, Winners, Bids, Comments, WatchList
# Register your models here.

admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Winners)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(WatchList)
