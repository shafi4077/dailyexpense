from django.contrib import admin

# Register your models here.
from .models import Transaction, MainCategory, SubCategory

admin.site.register(Transaction)
admin.site.register(MainCategory)
admin.site.register(SubCategory)