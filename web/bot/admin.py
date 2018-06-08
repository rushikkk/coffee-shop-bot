from django.contrib import admin

# Register your models here.
from .models import Coffee, Syrup, Size

admin.site.register(Coffee)
admin.site.register(Size)
admin.site.register(Syrup)
