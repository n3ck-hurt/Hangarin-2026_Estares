from django.contrib import admin
from .models import Category, Priority, Task, SubTask, Note

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_per_page = 20

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'color', 'created_at']
    list_editable = ['level', 'color']
    ordering = ['-level']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'category', 'due_date', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['status', 'priority']
    list_per_page = 25
    date_hierarchy = 'created_at'

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'task', 'order', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['status', 'order']
    list_per_page = 30

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['content_preview', 'task', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']
    list_per_page = 30
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content"