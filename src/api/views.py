from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Project, Issue, Comment, Contributor, CustomUser
from api.permissions import IsAuthenticatedProjectAuthorOrContributor
from api import serializers


class RegisterView(generics.CreateAPIView):
    """
    Class managing the following endpoint:
    /signup
    """
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegisterSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    """
    Class managing the following endpoint:
    /login
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.MyTokenObtainPairSerializer


class MultipleSerializerMixin:
    """
    Mixin allowing the change of a serializer_class in ViewSets.
    """
    detail_serializer_class = None

    def get_serializer_class(self):
        """
        Replaces standard serializer_class by a detail_serializer_class when viewing an object detail.
        """
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):
    """
    Class managing the following endpoints:
    /projects/:project_id/users/
    /projects/:project_id/users/:user_id
    """

    serializer_class = serializers.ContributorListSerializer
    permission_classes = [IsAuthenticatedProjectAuthorOrContributor]

    def get_queryset(self):
        """
        Defines the queryset.
        """
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        """
        Defines the creation [POST] of a contributor.
        Automatically saves the corresponding project and author of the contributor object.
        """
        user = get_object_or_404(CustomUser, pk=serializer._kwargs['data']['user_id'])
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        serializer.save(user=user, project=project)


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):
    """
    Class managing the following endpoints:
    /projects
    /projects/:project_id
    """

    serializer_class = serializers.ProjectListSerializer
    detail_serializer_class = serializers.ProjectDetailSerializer
    permission_classes = [IsAuthenticatedProjectAuthorOrContributor]

    def get_queryset(self):
        """
        Defines the queryset.
        """
        return Project.objects.all()

    def perform_create(self, serializer):
        """
        Defines the creation [POST] of a project.
        Automatically saves the corresponding author of the project.
        """
        serializer.save(author_user=self.request.user)


class IssueViewset(MultipleSerializerMixin, ModelViewSet):
    """
    Class managing the following endpoints:
    /projects/:project_id/issues
    /projects/:project_id/issues/:issue_id
    """

    serializer_class = serializers.IssueListSerializer
    detail_serializer_class = serializers.IssueDetailSerializer
    permission_classes = [IsAuthenticatedProjectAuthorOrContributor]

    def get_queryset(self):
        """
        Defines the queryset.
        """
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        """
        Defines the creation [POST] of an issue.
        Automatically saves the corresponding author and project of the issue.
        Also assigns the specified assigner user Foreign Key.
        """
        assignee_user = get_object_or_404(CustomUser, pk=serializer._kwargs['data']['assignee_user'])
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        serializer.save(author_user=self.request.user, assignee_user=assignee_user, project=project)

    def perform_update(self, serializer):
        """
        Re-defines the modification [PUT] of an issue.
        Allows the change of the specified assignee user Foreign Key.
        """
        assignee_user = get_object_or_404(CustomUser, pk=serializer._kwargs['data']['assignee_user'])
        serializer.save(assignee_user=assignee_user)


class CommentViewset(MultipleSerializerMixin, ModelViewSet):
    """
    Class managing the following endpoints:
    /projects/:project_id/issues/:issue_id/comments
    /projects/:project_id/issues/:issue_id/comments/:comment_id
    """

    serializer_class = serializers.CommentListSerializer
    detail_serializer_class = serializers.CommentDetailSerializer
    permission_classes = [IsAuthenticatedProjectAuthorOrContributor]

    def get_queryset(self):
        """
        Defines the queryset.
        """
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    def perform_create(self, serializer):
        """
        Defines the creation [POST] of a comment.
        Automatically saves the corresponding author and issue of the comment.

        As the description is only shown in a comment details through a 'retrieve' action, description is added to the
        creation process.
        """
        issue = get_object_or_404(Issue, pk=self.kwargs['issue_pk'])
        description = serializer._kwargs['data']['description']
        serializer.save(author_user=self.request.user, issue=issue, description=description)
