from django.contrib import admin
from .models import Organization, OrganizationMember

# Register your models here
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address")
    search_fields = ("name",)

class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "organization", "role")
    list_filter = ("role",)
    search_fields = ("user__email", "organization__name")

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationMember, OrganizationMemberAdmin)