from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Region, Table


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("user_name", "is_staff", "is_active", "role",)  # Добавляем role сюда
    list_filter = ("user_name", "is_staff", "is_active", "role",)  # И сюда
    fieldsets = (
        (None, {"fields": ("user_name", "password", "role",)}),  # И сюда
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "user_name", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions", "role",  # И сюда
            )}
        ),
    )
    search_fields = ("user_name",)
    ordering = ("user_name",)


class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "display_users")  # Показываем название и пользователей
    search_fields = ("name",)
    
    def display_users(self, obj):
        return ", ".join([user.user_name for user in obj.users.all()])
    display_users.short_description = "Associated Users"


class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "calendar", "article_сriminal_сode", "performance", "date_referral", "where_order_sent", "review_period", "response_received", "submissions_reviewed_deadline", "region_display")
    list_filter = ("performance", "where_order_sent", "review_period", "region")
    search_fields = ("number", "article_сriminal_сode")
    date_hierarchy = "calendar"

    def region_display(self, obj):
        return obj.region.name
    region_display.short_description = "Region"

    def get_readonly_fields(self, request, obj=None):
        if obj:  # When editing
            return self.readonly_fields + ("submissions_reviewed_deadline",)
        return self.readonly_fields


admin.site.register(Table, TableAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
