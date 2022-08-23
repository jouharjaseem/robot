from django.contrib import admin
from .models import Person
# Register your models here.
class Cateadmin(admin.ModelAdmin):
    list_display = ['content']
admin.site.register(Person,Cateadmin)