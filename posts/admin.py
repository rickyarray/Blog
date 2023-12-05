from django.contrib import admin
from .models import Post
from .views import Post

# Register your models here.
admin.site.register(Post)