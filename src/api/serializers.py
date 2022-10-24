from rest_framework.serializers import ModelSerializer, SerializerMethodField

from api.models import Projects, Issues, Comments, Contributors


class UserSerializer(ModelSerializer):

    class Meta:
        model = Contributors
        fields = ["id", "username", "email"]


class ContributorSerializer(ModelSerializer):

    users = SerializerMethodField()

    class Meta:
        model = Contributors
        fields = ["id", "permission", "role", 'users']

    def get_users(self, instance):
        queryset = instance.users.all()
        serializer = UserSerializer(queryset, many=True)
        return serializer.data


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comments
        fields = ["id", "issue_id", "author_user_id", "description", "created_time"]


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = ["id", "title", "description", "tag", "priority", "status", "project_id",
                  "author_user_id",
                  "assignee_user_id",
                  "created_time"]


class IssueDetailSerializer(ModelSerializer):

    comments = SerializerMethodField()

    class Meta:
        model = Issues
        fields = ["id", "title", "description", "tag", "priority", "status", "project_id",
                  "author_user_id",
                  "assignee_user_id",
                  "created_time",
                  "comments"]

    def get_comments(self, instance):
        queryset = instance.comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Projects
        fields = ["id", "title", "description", "type", "author_user_id"]


class ProjectDetailSerializer(ModelSerializer):

    issues = SerializerMethodField()

    class Meta:
        model = Projects
        fields = ["id", "title", "description", "type", "author_user_id", "issues"]

    def get_issues(self, instance):
        queryset = instance.issues.all()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data