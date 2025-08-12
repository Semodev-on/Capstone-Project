from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    def profile_pic_tag(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="width:50px; height:50px; border-radius:50%;" />', obj.profile_picture.url)
        return "No Image"
    profile_pic_tag.short_description = 'Profile Picture'

    list_display = [
        'username', 'email', 'first_name', 'last_name', 'gender', 'position',
        'institutional_school', 'contact_number', 'is_staff', 'profile_pic_tag'
    ]
    list_filter = ['gender', 'position', 'institutional_school', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'institutional_school']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('middle_name', 'gender', 'position', 'institutional_school', 'contact_number', 'profile_picture')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('first_name', 'middle_name', 'last_name', 'gender', 'position', 'institutional_school', 'contact_number', 'email', 'profile_picture')
        }),
    )