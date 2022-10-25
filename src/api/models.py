from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from issuetracking import settings


class CustomUser(AbstractUser):
    """Class User."""
    pass


class Project(models.Model):

    class Type(models.TextChoices):
        BACK_END = 'BE', _('Back-End')
        FRONT_END = 'FE', _('Front-End')
        IOS = 'IOS', _('iOS')
        ANDROID = "AN", _('Android')

    project_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    type = models.CharField(max_length=3, choices=Type.choices)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Author"
    )

    def __str__(self):
        return f"{self.title}"


class Issue(models.Model):

    class Tag(models.TextChoices):
        BUG = 'B', _('Bug')
        IMPROVEMENT = 'I', _('Improvement')
        TASK = 'T', _('Task')

    class Priority(models.TextChoices):
        LOW = 'L', _('Low')
        MEDIUM = 'M', _('Medium')
        HIGH = 'H', _('High')

    class Status(models.TextChoices):
        TO_DO = 'TD', _('To do')
        IN_PROGRESS = 'IP', _('In progress')
        COMPLETED = 'C', _('Completed')

    issue_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    tag = models.CharField(max_length=1, choices=Tag.choices)
    priority = models.CharField(max_length=1, choices=Priority.choices)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, verbose_name="project", related_name="issues")
    status = models.CharField(max_length=2, choices=Status.choices)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_issues",
        verbose_name="Author"
    )
    assignee_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assignee_issues",
        verbose_name="Assignee"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Contributor(models.Model):

    class Permission(models.TextChoices):
        CR = 'CR', _('Create and Read')
        CRUD = 'CRUD', _('Create, Read, Update and Delete')

    class Role(models.TextChoices):
        LEADER = 'L', _('Leader')
        DEVELOPER = 'D', _('Developer')
        TESTER = 'T', _('Tester')

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        verbose_name="Project",
        related_name='contributors'
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User",
        related_name='contributors'
    )
    permission = models.CharField(max_length=50, choices=Permission.choices)
    role = models.CharField(max_length=50, choices=Role.choices)


class Comment(models.Model):

    comment_id = models.BigAutoField(primary_key=True)
    description = models.fields.CharField(max_length=2048, verbose_name="Description")
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Author")
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, verbose_name="Issue", related_name="comments")
    created_time = models.DateTimeField(auto_now_add=True)
