from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError, CharField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import Project, Issue, Comment, Contributor, CustomUser


def contributor(user, project):
    """Verifies if a user is a contributor of the project."""

    try:
        Contributor.objects.get(user=user, project=project)
    except Contributor.DoesNotExist:
        return False
    else:
        return True


class RegisterSerializer(ModelSerializer):
    """Registration serializer."""

    password = CharField(write_only=True, required=True, validators=[validate_password])
    password_confirmation = CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password', 'password_confirmation')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        """Validates identical passwords."""

        if attrs['password'] != attrs['password_confirmation']:
            raise ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """Creates a custom user."""

        user = CustomUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom ObtainTokenPair Serializer from simple JWT to add a custom claim."""

    @classmethod
    def get_token(cls, user):
        """Gets token and add a claim."""
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claim
        token['email'] = user.email
        return token


class UserSerializer(ModelSerializer):
    """User serializer"""

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]


class ContributorDetailSerializer(ModelSerializer):
    """Contributor serializer for a specific detailed contributor."""

    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = ["user_id", "project_id", "permission", "role", 'user']


class ContributorListSerializer(ModelSerializer):
    """Contributor serializer for a list of contributors."""

    class Meta:
        model = Contributor
        fields = ["id", "user_id", "permission", "role"]


class CommentListSerializer(ModelSerializer):
    """Comment serializer for a list of comments."""

    class Meta:
        model = Comment
        fields = ["comment_id", "description", "author_user_id"]


class CommentDetailSerializer(ModelSerializer):
    """Comment serializer for a specific detailed comment."""

    class Meta:
        model = Comment
        fields = ["comment_id", "description", "issue_id", "author_user_id", "created_time"]


class IssueListSerializer(ModelSerializer):
    """Issue serializer for a list of issues."""

    class Meta:
        model = Issue
        fields = [
            "issue_id",
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "author_user_id",
            "assignee_user_id",
        ]

    def validate(self, data):
        """
        Verifies if an assignee user is part of the project contributors.
        If he is not, returns an error.
        """

        request = self.context.get("request")
        project = Project.objects.get(pk=request.parser_context['kwargs']['project_pk'])
        try:
            assignee_user = CustomUser.objects.get(pk=self._kwargs['data']['assignee_user'])
        except ObjectDoesNotExist:
            raise ValidationError(f"{self._kwargs['data']['assignee_user']} does not match any user id.")
        if not (contributor(assignee_user, project) or assignee_user == project.author_user):
            raise ValidationError(f"assignee_user {assignee_user.user_id} is no author nor contributor of this project")
        return data


class IssueDetailSerializer(ModelSerializer):
    """Issue serializer for a specific detailed issue."""

    comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            "issue_id",
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "project_id",
            "author_user_id",
            "assignee_user_id",
            "created_time",
            "comments"
        ]

    def get_comments(self, instance):
        """Gets a list of comments for a particular issue."""

        queryset = instance.comments.all()
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data


class ProjectListSerializer(ModelSerializer):
    """Project serializer for a list of projects."""

    class Meta:
        model = Project
        fields = ["project_id", "title", "description", "type", "author_user_id"]


class ProjectDetailSerializer(ModelSerializer):
    """Project serializer for a specific detailed project."""

    issues = SerializerMethodField()
    users = SerializerMethodField()

    class Meta:
        model = Project
        fields = ["project_id", "title", "description", "type", "author_user_id", "users", "issues"]

    def get_issues(self, instance):
        """Gets a list of issues for a particular project."""

        queryset = instance.issues.all()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data

    def get_users(self, instance):
        """Gets a list of contributors for a particular project."""

        queryset = instance.contributors.all()
        serializer = ContributorListSerializer(queryset, many=True)
        return serializer.data
