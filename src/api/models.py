from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from issuetracking import settings


class CustomUserManager(BaseUserManager):
    """Manager class for custom users."""

    def create_user(self, email: str, first_name: str, last_name: str, password=None):
        """
        Creates and saves a User with the given email, first name, last name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email: str, first_name: str, last_name: str, password: str):
        """
        Creates and saves a staff user with the given email, first name, last name and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, first_name: str, last_name: str, password: str):
        """
        Creates and saves a superuser with the given email, first name, last name and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """Class managing custom users."""

    class Meta:
        verbose_name = "User"

    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)

    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):
        return self.get_full_name()

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """
        Is the user a member of staff?
        """
        return self.staff

    @property
    def is_admin(self):
        """
        Is the user an admin member?
        """
        return self.admin


class Project(models.Model):
    """Class managing projects."""
    class Type(models.TextChoices):
        BACK_END = 'BE', _('Back-End')
        FRONT_END = 'FE', _('Front-End')
        IOS = 'IOS', _('iOS')
        ANDROID = "AN", _('Android')

    project_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=3, choices=Type.choices)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Author"
    )

    objects = models.Manager()

    def __str__(self):
        return f"{self.title}"


class Issue(models.Model):
    """Class managing issues."""

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
    description = models.CharField(max_length=2048)
    tag = models.CharField(max_length=1, choices=Tag.choices)
    priority = models.CharField(max_length=1, choices=Priority.choices)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="issues")
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
        verbose_name="Assignee",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.title}"


class Contributor(models.Model):
    """Class managing contributors. Represents a link between users and projects."""

    class Permission(models.TextChoices):
        ADMIN = 'A', _('Admin')
        RESTRICTED = 'R', _('Restricted access')
        MEMBER = 'M', _('Member')

    class Role(models.TextChoices):
        LEADER = 'L', _('Leader')
        DEVELOPER = 'D', _('Developer')
        TESTER = 'T', _('Tester')

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='contributors'
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contributors'
    )
    permission = models.CharField(max_length=50, choices=Permission.choices)
    role = models.CharField(max_length=50, choices=Role.choices)

    objects = models.Manager()


class Comment(models.Model):
    """Class managing comments."""

    comment_id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=2048)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Author")
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name="comments")
    created_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
