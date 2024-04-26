from django.contrib import admin

from .models import Genre, Category, Title, Review, Comment

admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
