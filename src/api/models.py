from django.contrib.auth.models import AbstractUser
from django.db import models

from issuetracking import settings


class CustomUser(AbstractUser):
    """Class User."""
    pass


class Projects(models.Model):

    class Meta:
        verbose_name = 'Project'

    class Type(models.TextChoices):
        BACK_END = 'BE'
        FRONT_END = 'FE'
        IOS = 'IOS'
        ANDROID = "AN"

    title = models.fields.CharField(max_length=128)
    description = models.fields.CharField(max_length=2048, blank=True)
    type = models.fields.CharField(max_length=5, choices=Type.choices)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                       verbose_name="Author")

    def __str__(self):
        return f"{self.title}"


class Issues(models.Model):

    class Meta:
        verbose_name = 'Issue'

    class Tag(models.TextChoices):
        BUG = 'BUG'
        IMPROVEMENT = 'IMP'
        TASK = 'TASK'

    class Priority(models.TextChoices):
        LOW = 'LOW'
        MEDIUM = 'MED'
        HIGH = 'HIGH'

    class Status(models.TextChoices):
        TO_DO = 'TD'
        IN_PROGRESS = 'IP'
        COMPLETED = 'COMP'

    title = models.fields.CharField(max_length=128)
    description = models.fields.CharField(max_length=2048, blank=True)
    tag = models.fields.CharField(max_length=5, choices=Tag.choices)
    priority = models.CharField(max_length=128, choices=Priority.choices)
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE, verbose_name="Project")
    status = models.CharField(max_length=128, choices=Status.choices)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                       related_name="author_issues", verbose_name="Author")
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                         related_name="assignee_issues", verbose_name="Assignee")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Contributors(models.Model):

    class Meta:
        verbose_name = 'Contributor'

    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE, verbose_name="Project")
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    permission = models.CharField(max_length=128)
    role = models.CharField(max_length=128)


class Comments(models.Model):

    class Meta:
        verbose_name = 'Comment'

    description = models.fields.CharField(max_length=2048, verbose_name="Description")
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                       verbose_name="Author")
    issue_id = models.ForeignKey(to=Issues, on_delete=models.CASCADE, verbose_name="Issue")
    created_time = models.DateTimeField(auto_now_add=True)
