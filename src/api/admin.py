from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import Project, Issue, Contributor, Comment, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """CustomUser class."""

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'first_name', 'last_name', 'admin', 'staff', 'is_active']
    list_filter = ['admin', 'staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


@admin.register(Project)
class ProjectsAdmin(admin.ModelAdmin):

    list_display = ("title", "type", "author_user")
    autocomplete_fields = ("author_user",)
    search_fields = ("project",)


@admin.register(Issue)
class IssuesAdmin(admin.ModelAdmin):

    list_display = ("title", "tag", "priority", "status", "project", "created_time")
    autocomplete_fields = ("project", "author_user", "assignee_user")
    search_fields = ("issue",)


@admin.register(Contributor)
class ContributorsAdmin(admin.ModelAdmin):

    list_display = ("project", "user", "permission", "role")
    autocomplete_fields = ("project", "user")


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):

    list_display = ("project", "issue", "author_user", "created_time")
    autocomplete_fields = ("author_user", "issue")

    @admin.display(description='Project')
    def project(self, obj):
        return obj.issue.project
