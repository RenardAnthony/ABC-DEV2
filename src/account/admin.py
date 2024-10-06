from django.contrib import admin

# Register your models here.
from account.models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "pseudo",
        "email",
        "is_active",
    )
    list_per_page = 30

