from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Feature


class VotesFilter(admin.SimpleListFilter):
    title = "Votes"
    parameter_name = "votes"

    def lookups(self, request, model_admin):
        return [
            ("0", "0 votes"),
            ("1-4", "1–4 votes"),
            ("5-9", "5–9 votes"),
            ("10+", "10+ votes"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "0":
            return queryset.filter(votes=0)
        elif value == "1-4":
            return queryset.filter(votes__gte=1, votes__lte=4)
        elif value == "5-9":
            return queryset.filter(votes__gte=5, votes__lte=9)
        elif value == "10+":
            return queryset.filter(votes__gte=10)
        return queryset


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Feature model with custom functionality.
    """

    # List display configuration
    list_display = [
        "title_with_link",
        "description_preview",
        "votes_badge",
        "created_at_formatted",
        "updated_at_formatted",
        "quick_actions",
    ]

    # List filters
    list_filter = [
        "created_at",
        "updated_at",
        VotesFilter,
    ]

    # Search functionality
    search_fields = ["title", "description"]

    # Ordering
    # ordering = ["-votes", "-created_at"]

    # Read-only fields
    readonly_fields = ["id", "votes", "created_at", "updated_at", "votes_chart"]

    # Fieldsets for organized form layout
    fieldsets = (
        ("Feature Information", {"fields": ("title", "description")}),
        ("Statistics", {"fields": ("votes", "votes_chart"), "classes": ("collapse",)}),
        (
            "Metadata",
            {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    # Actions
    actions = ["reset_votes", "add_vote", "feature_popular"]

    def title_with_link(self, obj):
        """Display title with link to detail view."""
        url = reverse("admin:features_feature_change", args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.title)

    title_with_link.short_description = "Title"
    title_with_link.admin_order_field = "title"

    def description_preview(self, obj):
        """Show truncated description with tooltip."""
        if obj.description:
            preview = (
                obj.description[:50] + "..."
                if len(obj.description) > 50
                else obj.description
            )
            return format_html('<span title="{}">{}</span>', obj.description, preview)
        return format_html('<em style="color: #999;">No description</em>')

    description_preview.short_description = "Description"

    def votes_badge(self, obj):
        """Display votes with colored badge."""
        vote_count = obj.vote_count
        if vote_count >= 10:
            color = "#28a745"  # Green for popular
        elif vote_count >= 5:
            color = "#ffc107"  # Yellow for moderate
        else:
            color = "#6c757d"  # Gray for low votes

        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 12px; font-size: 12px; font-weight: bold;">{} votes</span>',
            color,
            vote_count,
        )

    votes_badge.short_description = "Votes"

    def created_at_formatted(self, obj):
        """Format creation date nicely."""
        return obj.created_at.strftime("%b %d, %Y at %I:%M %p")

    created_at_formatted.short_description = "Created"
    created_at_formatted.admin_order_field = "created_at"

    def updated_at_formatted(self, obj):
        """Format update date nicely."""
        return obj.updated_at.strftime("%b %d, %Y at %I:%M %p")

    updated_at_formatted.short_description = "Updated"
    updated_at_formatted.admin_order_field = "updated_at"

    def quick_actions(self, obj):
        """Quick action buttons."""
        return format_html(
            '<a class="button" href="#" onclick="addVote(\'{}\'); return false;" '
            'style="background: #007cba; color: white; padding: 5px 10px; '
            'text-decoration: none; border-radius: 3px; font-size: 11px;">+1 Vote</a>',
            obj.pk,
        )

    quick_actions.short_description = "Actions"

    def votes_chart(self, obj):
        """Simple visual representation of votes."""
        vote_count = obj.vote_count
        if vote_count == 0:
            return "No votes yet"

        # Create a simple bar chart using HTML/CSS
        max_width = 200
        bar_width = min(vote_count * 10, max_width)

        return format_html(
            '<div style="background: #e9ecef; width: {}px; height: 20px; border-radius: 10px;">'
            '<div style="background: linear-gradient(90deg, #007cba, #28a745); '
            "width: {}px; height: 20px; border-radius: 10px; display: flex; "
            'align-items: center; justify-content: center; color: white; font-size: 11px;">'
            "{} votes</div></div>",
            max_width,
            bar_width,
            vote_count,
        )

    votes_chart.short_description = "Vote Visualization"

    # Custom actions
    def reset_votes(self, request, queryset):
        """Reset votes to 0 for selected features."""
        updated = queryset.update(votes=0)
        self.message_user(
            request, f"Successfully reset votes for {updated} feature(s)."
        )

    reset_votes.short_description = "Reset votes to 0"

    def add_vote(self, request, queryset):
        """Add one vote to selected features."""
        for feature in queryset:
            feature.upvote()
        self.message_user(
            request, f"Successfully added 1 vote to {queryset.count()} feature(s)."
        )

    add_vote.short_description = "Add 1 vote to selected features"

    def feature_popular(self, request, queryset):
        """Mark features as popular (set votes to 10)."""
        updated = queryset.update(votes=10)
        self.message_user(
            request, f"Successfully marked {updated} feature(s) as popular."
        )

    feature_popular.short_description = "Mark as popular (10 votes)"

    class Media:
        """Add custom CSS and JavaScript."""

        css = {"all": ("admin/css/custom_admin.css",)}
        js = ("admin/js/custom_admin.js",)


# Customize admin site headers
admin.site.site_header = "Feature Voting System Admin"
admin.site.site_title = "Feature Voting Admin"
admin.site.index_title = "Welcome to Feature Voting System Administration"
