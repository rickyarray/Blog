from django.contrib import admin
from .models import Post, Status
from .views import Post


# Register your models here.
admin.site.register(Post)
admin.site.register(Status)
