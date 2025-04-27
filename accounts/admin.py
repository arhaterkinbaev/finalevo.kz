from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('username', 'email', 'is_staff', 'is_active', 'profile_picture_display')
    list_filter = ('is_staff', 'is_active', 'is_superuser')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_picture')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'bio', 'profile_picture')}),
    )

    def profile_picture_display(self, obj):
        if obj.profile_picture:
            return f"<img src='{obj.profile_picture.url}' width='50' height='50' style='border-radius:50%;' />"
        return "No Image"
    profile_picture_display.allow_tags = True
    profile_picture_display.short_description = 'Profile Picture'

# Регистрация модели CustomUser
admin.site.register(CustomUser, CustomUserAdmin)

# Регистрация модели Product (если используем)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
