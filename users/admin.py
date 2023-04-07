from django.contrib import admin

from users.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(StepOrder)
admin.site.register(WayOrder)
admin.site.register(Order)
admin.site.register(BookOrder)
admin.site.register(Basket)