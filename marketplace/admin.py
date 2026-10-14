from django.contrib import admin
from .models import Category, Item, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'price', 'category', 'listing_type', 'is_available', 'created_at']
    list_filter = ['listing_type', 'is_available', 'category', 'condition']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['item', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['comment', 'reviewer__username', 'item__title']
