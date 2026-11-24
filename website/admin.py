from django.contrib import admin
from django.utils.html import format_html
from .models import CompanySetting, Service, Project, Contact, Blog, Testimonial, Newsletter


@admin.register(CompanySetting)
class CompanySettingAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'phone', 'business_hours')

    fieldsets = (
        ("Company Identity & Homepage Hero", {
            "fields": ("company_name", "headline", "supporting_text"),
            "description": "Core company brand text displayed in the homepage hero and navigation."
        }),
        ("Contact Details & Operating Hours", {
            "fields": ("email", "phone", "address", "business_hours"),
            "description": "Leave phone or hours empty if unconfirmed. They will be automatically hidden from public pages."
        }),
        ("Social Profiles", {
            "fields": ("linkedin_url", "twitter_url", "github_url", "facebook_url", "instagram_url", "youtube_url"),
            "description": "Empty URLs are automatically hidden across the site."
        }),
    )

    def has_add_permission(self, request):
        return not CompanySetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'stage_badge', 'order', 'is_active', 'has_demo', 'has_screenshot')
    list_editable = ('order', 'is_active')
    list_filter = ('stage', 'is_active')
    search_fields = ('title', 'subtitle', 'description', 'modules')

    fieldsets = (
        ("Product Information", {
            "fields": ("title", "subtitle", "stage", "technology", "order", "is_active"),
        }),
        ("Product Scope & Module List", {
            "fields": ("description", "modules"),
            "description": "List each module on a new line so it renders cleanly as a feature list."
        }),
        ("Media & Links", {
            "fields": ("image", "live_demo", "github"),
            "description": "Leave 'live_demo' blank until a real demo URL is available. Do not use fake demo links."
        }),
    )

    @admin.display(description="Development Stage")
    def stage_badge(self, obj):
        colors = {
            'planning': '#6c757d',
            'in_development': '#0d6efd',
            'ready_to_demo': '#198754',
            'live': '#20c997',
        }
        color = colors.get(obj.stage, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 4px; font-weight: 500;">{}</span>',
            color,
            obj.get_stage_display()
        )

    @admin.display(boolean=True, description="Demo URL")
    def has_demo(self, obj):
        return bool(obj.live_demo)

    @admin.display(boolean=True, description="Screenshot")
    def has_screenshot(self, obj):
        return bool(obj.image)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order', 'is_active', 'support_hours_published', 'response_commitment_published')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')

    fieldsets = (
        ("Service Details", {
            "fields": ("title", "icon", "description", "order", "is_active"),
            "description": "Icon class format: Bootstrap icon name (e.g. 'bi bi-laptop', 'bi bi-tools', 'bi bi-diagram-3', 'bi bi-headset')."
        }),
        ("Confirmed Commitments", {
            "fields": ("support_hours", "response_commitment"),
            "description": "Leave blank if unconfirmed. Only published commitments appear on the website."
        }),
    )

    @admin.display(boolean=True, description="Support Hours")
    def support_hours_published(self, obj):
        return bool(obj.support_hours)

    @admin.display(boolean=True, description="Response Commitment")
    def response_commitment_published(self, obj):
        return bool(obj.response_commitment)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'email', 'phone', 'status_badge', 'email_backend_status', 'created')
    list_filter = ('status', 'email_sent', 'created')
    list_editable = ()
    search_fields = ('name', 'email', 'phone', 'topic', 'message')
    readonly_fields = ('name', 'email', 'phone', 'topic', 'message', 'created', 'email_sent', 'email_error')

    fieldsets = (
        ("Enquiry Status & Workflow", {
            "fields": ("status",),
            "description": "Update status to Contacted when following up with the client, and Closed once complete."
        }),
        ("Enquiry Details", {
            "fields": ("topic", "name", "email", "phone", "message", "created"),
        }),
        ("Email Backend Hand-off Diagnostics", {
            "fields": ("email_sent", "email_error"),
            "description": (
                "Accepted by Backend confirms that Django's configured mail backend accepted the message. "
                "Final inbox delivery and reply-to routing require verified production SMTP credentials."
            )
        }),
    )

    @admin.display(description="Status")
    def status_badge(self, obj):
        colors = {
            'new': '#dc3545',
            'contacted': '#0d6efd',
            'closed': '#198754',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; border-radius: 4px; font-weight: 600;">{}</span>',
            color,
            obj.get_status_display()
        )

    @admin.display(description="Email Backend Status")
    def email_backend_status(self, obj):
        if obj.email_sent:
            return format_html(
                '<span style="color: #198754; font-weight: bold;" title="Message accepted by configured email backend (console/SMTP).">✔ Accepted by Backend</span>'
            )
        if obj.email_error:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;" title="{}">✖ Failed (Check diagnostics)</span>',
                obj.email_error[:100]
            )
        return format_html('<span style="color: #ffc107; font-weight: bold;">Pending / Not Dispatched</span>')


admin.site.register(Blog)
admin.site.register(Testimonial)
admin.site.register(Newsletter)
