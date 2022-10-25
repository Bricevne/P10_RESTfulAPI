from rest_framework.serializers import ModelSerializer, SerializerMethodField

from api.models import Project, Issue, Comment, Contributor, CustomUser


class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email"]


class ContributorDetailSerializer(ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = ["id", "permission", "role", 'user']


class ContributorListSerializer(ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = ['user']


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["comment_id", "issue", "author_user", "description", "created_time"]


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ["issue_id", "title", "description", "tag", "priority", "status", "project",
                  "author_user",
                  "assignee_user",
                  "created_time"]


class IssueDetailSerializer(ModelSerializer):

    comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = ["issue_id", "title", "description", "tag", "priority", "status", "project",
                  "author_user",
                  "assignee_user",
                  "created_time",
                  "comments"]

    def get_comments(self, instance):
        queryset = instance.comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ["project_id", "title", "description", "type", "author_user"]


class ProjectDetailSerializer(ModelSerializer):

    issues = SerializerMethodField()
    users = SerializerMethodField()

    class Meta:
        model = Project
        fields = ["project_id", "title", "description", "type", "author_user", "users", "issues"]

    def get_issues(self, instance):
        queryset = instance.issues.all()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data

    def get_users(self, instance):
        queryset = instance.contributors.all()
        serializer = ContributorListSerializer(queryset, many=True)
        return serializer.data
