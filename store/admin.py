from django.contrib import admin
from .models import *


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Whishlist)
admin.site.register(Order)
admin.site.register(OrderedItem)
admin.site.register(Profile)


