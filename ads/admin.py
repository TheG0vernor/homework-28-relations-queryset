from django.contrib import admin

from ads.models import Location, User, Category, Ad

# Register your models here.
admin.site.register(Location)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Ad)
