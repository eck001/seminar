from django.contrib import admin

from .models import *

# Register your models here.

class page1Admin(admin.ModelAdmin):
    pass
admin.site.register(Tweets, page1Admin)
admin.site.register(details, page1Admin)
