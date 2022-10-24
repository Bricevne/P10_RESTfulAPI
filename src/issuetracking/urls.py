"""issuetracking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import ProjectViewset, IssueViewset, CommentViewset, ContributorViewset

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewset, basename="project")

projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(r'issues', IssueViewset, basename='project-issues')

users_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
users_router.register(r'users', ContributorViewset, basename='project-users')

issues_router = routers.NestedSimpleRouter(projects_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewset, basename='issue-comments')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair_view'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_obtain_pair_view'),
    path(r'', include(router.urls)),
    path(r'', include(projects_router.urls)),
    path(r'', include(users_router.urls)),
    path(r'', include(issues_router.urls))
]
