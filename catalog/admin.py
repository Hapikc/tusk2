from django.contrib import admin
from .models import AdvUser
from .models import Categories
from .models import Application


class ApplicationAdmin(admin.ModelAdmin):
    model = Application
    list_display = ('name', 'description', 'price', 'photo', 'status', 'date')

admin.site.register(AdvUser)
admin.site.register(Categories)
admin.site.register(Application, ApplicationAdmin)
