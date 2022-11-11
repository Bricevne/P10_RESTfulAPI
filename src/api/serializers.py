from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError, CharField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import Project, Issue, Comment, Contributor, CustomUser

def contributor(user, project):
    try:
        Contributor.objects.get(user=user, project=project)
    except Contributor.DoesNotExist:
        return False
    else:
        return True

class RegisterSerializer(ModelSerializer):

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
        if attrs['password'] != attrs['password_confirmation']:
            raise ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):

        user = CustomUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        return token


class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]


class ContributorDetailSerializer(ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = ["user_id", "project_id", "permission", "role", 'user']


class ContributorListSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ["id", "user_id", "permission", "role"]


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["comment_id", "description", "author_user_id"]


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["comment_id", "description", "issue_id", "author_user_id", "created_time"]


class IssueListSerializer(ModelSerializer):
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
        request = self.context.get("request")
        project = Project.objects.get(pk=request.parser_context['kwargs']['project_pk'])
        assignee_user = CustomUser.objects.get(pk=self._kwargs['data']['assignee_user'])
        if not (contributor(assignee_user, project) or assignee_user == project.author_user):
            raise ValidationError(f"assignee_user {assignee_user.user_id} is no author nor contributor of this project")
        return data


class IssueDetailSerializer(ModelSerializer):

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
        queryset = instance.comments.all()
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ["project_id", "title", "description", "type", "author_user_id"]


class ProjectDetailSerializer(ModelSerializer):

    issues = SerializerMethodField()
    users = SerializerMethodField()

    class Meta:
        model = Project
        fields = ["project_id", "title", "description", "type", "author_user_id", "users", "issues"]

    def get_issues(self, instance):
        queryset = instance.issues.all()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data

    def get_users(self, instance):
        queryset = instance.contributors.all()
        serializer = ContributorListSerializer(queryset, many=True)
        return serializer.data
