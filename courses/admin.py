from django.contrib import admin
from .models import Section, Material

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('owner',)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'owner', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('section', 'owner')
