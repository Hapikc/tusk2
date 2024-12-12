from django.contrib import admin
from .models import AdvUser
from .models import Categories
from .models import Application


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'status')

admin.site.register(AdvUser)
admin.site.register(Categories)
admin.site.register(Application, ApplicationAdmin)
