from django.contrib import admin

from .models import Visit


admin.site.site_header = "Xselid Studio - Администрирование"
admin.site.site_title = "Xselid Studio Admin"
admin.site.index_title = "Панель управления"


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("created_at", "path", "method", "ip_address", "short_user_agent")
    list_filter = ("method", "created_at")
    search_fields = ("path", "ip_address", "user_agent", "referer")
    readonly_fields = (
        "path",
        "method",
        "user_agent",
        "ip_address",
        "referer",
        "created_at",
    )
    ordering = ("-created_at",)
    list_per_page = 50 
    date_hierarchy = "created_at" 

    def short_user_agent(self, obj):
        ua = obj.user_agent or ""
        return ua[:80] + ("..." if len(ua) > 80 else "")

    short_user_agent.short_description = "User-Agent"
