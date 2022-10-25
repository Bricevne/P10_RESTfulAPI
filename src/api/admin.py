from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import Project, Issue, Contributor, Comment, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """CustomUser class."""
    pass


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
