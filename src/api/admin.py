from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import Projects, Issues, Contributors, Comments, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """CustomUser class."""
    pass


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):

    list_display = ("title", "type", "author_user_id")
    autocomplete_fields = ("author_user_id",)
    search_fields = ("project_id",)


@admin.register(Issues)
class IssuesAdmin(admin.ModelAdmin):

    list_display = ("title", "tag", "priority", "status", "project_id", "created_time")
    autocomplete_fields = ("project_id", "author_user_id", "assignee_user_id")
    search_fields = ("issue_id",)


@admin.register(Contributors)
class ContributorsAdmin(admin.ModelAdmin):

    list_display = ("project_id", "user_id", "permission", "role")
    autocomplete_fields = ("project_id", "user_id")


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):

    list_display = ("project", "issue_id", "author_user_id", "created_time")
    autocomplete_fields = ("author_user_id", "issue_id")

    @admin.display(description='Project')
    def project(self, obj):
        return obj.issue_id.project_id
