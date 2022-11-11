from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Project, Issue, Comment, Contributor, CustomUser
from api.permissions import IsAuthenticatedProjectAuthorOrContributor
from api.serializers import ProjectListSerializer, ProjectDetailSerializer, IssueListSerializer, \
    IssueDetailSerializer, ContributorListSerializer, ContributorDetailSerializer, CommentListSerializer, \
    CommentDetailSerializer, MyTokenObtainPairSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer
    permission_classes = [IsAuthenticatedProjectAuthorOrContributor]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        user = get_object_or_404(CustomUser, pk=serializer._kwargs['data']['user_id'])
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        serializer.save(user=user, project=project)


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticatedProjectAuthorOrContributor]

    def get_queryset(self):
        return Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(author_user=self.request.user)


class IssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticatedProjectAuthorOrContributor]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        assignee_user = get_object_or_404(CustomUser, pk=serializer._kwargs['data']['assignee_user'])
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        serializer.save(author_user=self.request.user, assignee_user=assignee_user, project=project)

    def perform_update(self, serializer):
        assignee_user = get_object_or_404(CustomUser, pk=serializer._kwargs['data']['assignee_user'])
        serializer.save(assignee_user=assignee_user)



class CommentViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticatedProjectAuthorOrContributor]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    def perform_create(self, serializer):
        issue = get_object_or_404(Issue, pk=self.kwargs['issue_pk'])
        description = serializer._kwargs['data']['description']
        serializer.save(author_user=self.request.user, issue=issue, description=description)