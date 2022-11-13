from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from api.models import Project, Contributor, Issue, Comment


def contributor(user, project):
    """Verifies if a user is a contributor of the project."""

    try:
        Contributor.objects.get(user=user, project=project)
    except Contributor.DoesNotExist:
        return False
    else:
        return True


class IsAuthenticatedProjectAuthorOrContributor(BasePermission):
    """
    Controls if the user has the right permissions to access the data.
    An authenticated user can create a project and access the list of projects.
    An authenticated user can access a project and its issues/contributors/comments only if he is a contributor
    of the project.
    An authenticated user can update and delete an object only if he is its author.
    """

    def has_permission(self, request, view):
        """
        Controls who has view permission on the corresponding view.
        """
        from api.views import ProjectViewset

        is_authenticated = bool(request.user and request.user.is_authenticated)

        if not is_authenticated:
            return False

        # if user is authenticated, can view projects list
        if isinstance(view, ProjectViewset) and view.action in ['list', 'create']:
            return True

        # Can access the project
        if isinstance(view, ProjectViewset):
            project = get_object_or_404(Project, pk=view.kwargs['pk'])
        else:
            project = get_object_or_404(Project, pk=view.kwargs['project_pk'])

        is_contributor = contributor(request.user, project)
        is_project_author = (request.user == project.author_user)

        if request.user and (is_contributor or is_project_author):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        Controls who has object level permissions on the corresponding object.
        """

        if isinstance(obj, Contributor) or isinstance(obj, Issue):
            project = obj.project
        elif isinstance(obj, Comment):
            project = obj.issue.project
        else:
            project = obj

        is_contributor = contributor(request.user, project)
        is_project_author = (request.user == project.author_user)

        if request.method in SAFE_METHODS \
                and request.user \
                and request.user.is_authenticated \
                and (is_contributor or is_project_author):
            return True

        if isinstance(obj, Contributor):
            instance = obj.project
        else:
            instance = obj
        is_author = bool(instance.author_user == request.user)
        return bool(request.user and request.user.is_authenticated and is_author)
