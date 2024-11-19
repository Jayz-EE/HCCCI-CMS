from django.contrib import admin
from .models import Page, GalleryImage

class GalleryInline(admin.TabularInline):
    model = GalleryImage
    extra = 1

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GalleryInline]  # Allows you to add galleries to the page directly
    search_fields = ['title', 'content']
    list_filter = ['created_at']

@admin.register(GalleryImage)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'page', 'image')
    list_filter = ['page']
