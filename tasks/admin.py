from django.contrib import admin
from .models import ArmoryCategory, Supplier, Weapon, Client, Transaction, IntelligenceNote

@admin.register(ArmoryCategory)
class ArmoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'reliability_score']
    search_fields = ['name', 'country']

@admin.register(Weapon)
class WeaponAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_number', 'category', 'unit_price', 'stock_quantity', 'is_active']
    list_filter = ['category', 'supplier', 'is_active']
    search_fields = ['name', 'model_number']
    list_editable = ['unit_price', 'stock_quantity', 'is_active']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'clearance_level', 'total_spent']
    list_filter = ['region', 'clearance_level']
    search_fields = ['name', 'region']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'weapon', 'quantity', 'total_price', 'status', 'deal_date']
    list_filter = ['status', 'deal_date']
    search_fields = ['client__name', 'weapon__name']
    list_editable = ['status']
    date_hierarchy = 'deal_date'

@admin.register(IntelligenceNote)
class IntelligenceNoteAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'content_preview', 'created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Intel Preview"