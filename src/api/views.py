from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import Projects, Issues, Comments
from api.serializers import ProjectSerializer, IssueSerializer, CommentSerializer


class ProjectViewset(ReadOnlyModelViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Projects.objects.all()


class IssueViewset(ReadOnlyModelViewSet):

    serializer_class = IssueSerializer

    def get_queryset(self):
        queryset = Issues.objects.all()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset


class CommentViewset(ReadOnlyModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comments.objects.all()
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset
