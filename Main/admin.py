from django.contrib import admin
from models import StockType, Category, Stock


class StockTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'alias', 'comment']
    search_fields = ['name', 'alias', 'comment']
    list_per_page = 50

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'alias', 'comment']
    search_fields = ['name', 'alias', 'comment']
    list_per_page = 50

class StockAdmin(admin.ModelAdmin):
    list_display = ['sid', 'name', 'category', 'address', 'web']
    list_filter = ['category']
    list_per_page = 100
    search_fields = ['sid', 'name']


admin.site.register(StockType, StockTypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Stock, StockAdmin)