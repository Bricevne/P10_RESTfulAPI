from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import Projects, Issues, Comments
from api.serializers import ProjectListSerializer, ProjectDetailSerializer, IssueListSerializer, CommentSerializer, \
    IssueDetailSerializer


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Projects.objects.all()


class IssueViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        queryset = Issues.objects.all()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset


class CommentViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comments.objects.all()
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset
