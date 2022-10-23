from rest_framework.serializers import ModelSerializer

from api.models import Projects, Issues, Comments


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Projects
        fields = ["id", "title", "description", "type", "author_user_id"]


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issues
        fields = ["id", "title", "description", "tag", "priority", "status", "project_id", "created_time"]


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comments
        fields = ["id", "issue_id", "author_user_id", "description", "created_time"]