from django.contrib import admin
from .models import Realtor, Property, CallRequest, Payment

@admin.register(Realtor)
class RealtorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'experience_years', 'is_active']
    list_filter = ['is_active', 'experience_years']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['created_at']

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'price', 'address', 'realtor', 'is_available']
    list_filter = ['property_type', 'is_available', 'realtor']
    search_fields = ['title', 'address', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CallRequest)
class CallRequestAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_phone', 'realtor', 'property', 'status', 'created_at']
    list_filter = ['status', 'realtor', 'created_at']
    search_fields = ['client_name', 'client_phone', 'message']
    readonly_fields = ['created_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['call_request', 'amount', 'status', 'created_at', 'paid_at']
    list_filter = ['status', 'created_at']
    search_fields = ['transaction_id']
    readonly_fields = ['created_at', 'paid_at']
