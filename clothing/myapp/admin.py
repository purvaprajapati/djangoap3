from django.contrib import admin
from .models import UserProfile, Blog, Contact, Clothes, Like, Comment

# Register all models here for Django Admin Panel
admin.site.register(UserProfile)
admin.site.register(Blog)
admin.site.register(Contact)
admin.site.register(Clothes)
admin.site.register(Like)
admin.site.register(Comment)