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


@admin.register(Issues)
class IssuesAdmin(admin.ModelAdmin):

    list_display = ("title", "tag", "priority", "status", "project_id", "created_time")


@admin.register(Contributors)
class ContributorsAdmin(admin.ModelAdmin):

    list_display = ("project_id", "user_id", "permission", "role")


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):

    list_display = ("author_user_id", "issue_id", "created_time")

# class ArticleAdmin(admin.ModelAdmin):
#
#     list_display = ('name', 'product', 'category', 'active')
#
#     @admin.display(description='Category')
#     def category(self, obj):
#         return obj.product.category
