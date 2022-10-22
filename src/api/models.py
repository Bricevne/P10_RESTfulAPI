from django.contrib.auth.models import AbstractUser
from django.db import models

from issuetracking import settings


class CustomUser(AbstractUser):
    """Class User."""
    pass


class Projects(models.Model):

    class Type(models.TextChoices):
        BACK_END = 'BE'
        FRONT_END = 'FE'
        IOS = 'IOS'
        ANDROID = "AN"

    title = models.fields.CharField(max_length=128, verbose_name="Titre")
    description = models.fields.CharField(max_length=2048, blank=True, verbose_name="Description")
    type = models.fields.CharField(max_length=5, choices=Type.choices, verbose_name="Type")
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class Issues(models.Model):

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

    title = models.fields.CharField(max_length=128, verbose_name="Titre")
    description = models.fields.CharField(max_length=2048, blank=True, verbose_name="Description")
    tag = models.fields.CharField(max_length=5, choices=Tag.choices, verbose_name="Tag")
    priority = models.CharField(max_length=128, choices=Priority.choices, verbose_name="Priorité")
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    status = models.CharField(max_length=128, choices=Status.choices)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                       related_name="author_issues")
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                         related_name="assignee_issues")
    created_time = models.DateTimeField(auto_now_add=True)


class Contributors(models.Model):
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permission = models.CharField(max_length=128)
    role = models.CharField(max_length=128)


class Comments(models.Model):
    description = models.fields.CharField(max_length=2048, verbose_name="Description")
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    issue_id = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
