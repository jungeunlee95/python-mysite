from django.contrib import admin

# Register your models here.
from guestbook.models import Guestbook

admin.site.register(Guestbook)