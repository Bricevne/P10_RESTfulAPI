from rest_framework.serializers import ModelSerializer, SerializerMethodField

from api.models import Projects, Issues, Comments


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comments
        fields = ["id", "issue_id", "author_user_id", "description", "created_time"]


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issues
        fields = ["id", "title", "description", "tag", "priority", "status", "project_id",
                  "author_user_id",
                  "assignee_user_id",
                  "created_time"]


class ProjectSerializer(ModelSerializer):

    issues = SerializerMethodField()

    class Meta:
        model = Projects
        fields = ["id", "title", "description", "type", "author_user_id", "issues"]

    def get_issues(self, instance):
        queryset = instance.issues.all()
        serializer = IssueSerializer(queryset, many=True)
        return serializer.data