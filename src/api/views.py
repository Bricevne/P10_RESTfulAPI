from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import Projects, Issues, Comments, Contributors
from api.serializers import ProjectListSerializer, ProjectDetailSerializer, IssueListSerializer, CommentSerializer, \
    IssueDetailSerializer, ContributorSerializer


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContributorViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributors.objects.filter(project_id=self.kwargs['project_pk'])


class ProjectViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Projects.objects.all()


class IssueViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issues.objects.filter(project_id=self.kwargs['project_pk'])


class CommentViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.filter(issue_id=self.kwargs['issue_pk'])

