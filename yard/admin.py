from django.contrib import admin
from .models import Car, CarInstance, Part, AssemblyGroup

admin.site.register(Car)
admin.site.register(CarInstance)
admin.site.register(Part)
admin.site.register(AssemblyGroup)
