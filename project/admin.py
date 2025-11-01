from django.contrib import admin
from .models import Category, Item, Sales, UserProfile

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Sales)
admin.site.register(UserProfile)
