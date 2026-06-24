from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Company)


admin.site.register(Product)


admin.site.register(Category)




admin.site.register(Customer)


admin.site.register(Company_Types)

admin.site.register(OrderItems)

admin.site.register(Orders)