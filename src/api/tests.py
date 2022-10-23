from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from api.models import Projects, CustomUser, Issues


class TrackingAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.first_user = CustomUser.objects.create(username="Brice", password="123123")
        cls.second_user = CustomUser.objects.create(username="Paul", password="123123")

        cls.first_project = Projects.objects.create(title='first_project', type='BE', author_user_id=cls.first_user)
        cls.second_project = Projects.objects.create(title='second_project', type='IOS', author_user_id=cls.second_user)

        cls.first_issue = cls.first_project.issues.create(
            title='first_issue',
            tag="BUG",
            priority='LOW',
            status="TD",
            author_user_id=cls.first_user,
            assignee_user_id = cls.first_user
        )

        cls.second_issue = cls.first_project.issues.create(
            title='second_issue',
            tag="IMP",
            description="description",
            priority='MED',
            status="IP",
            author_user_id=cls.first_user,
            assignee_user_id=cls.second_user
        )

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def get_issue_list_data(self, issues):
        return [
            {
                'id': issue.pk,
                'title': issue.title,
                'description': issue.description,
                'tag': issue.tag,
                'project_id': issue.project_id.pk,
                'priority': issue.priority,
                'status': issue.status,
                'author_user_id': issue.author_user_id.pk,
                'assignee_user_id': issue.assignee_user_id.pk,
                'created_time': self.format_datetime(issue.created_time)
            } for issue in issues
        ]

    def get_project_list_data(self, projects):
        return [
            {
                'id': project.pk,
                'title': project.title,
                'description': project.description,
                'type': project.type,
                'author_user_id': project.author_user_id.pk,
                'issues': self.get_issue_list_data(project.issues.all())
            } for project in projects
        ]


class TestProject(TrackingAPITestCase):

    url = reverse_lazy('project-list')

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        excepted = self.get_project_list_data([self.first_project, self.second_project])
        self.assertEqual(excepted, response.json()['results'])


class TestIssue(TrackingAPITestCase):

    url = reverse_lazy('issue-list')

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        excepted = self.get_issue_list_data([self.first_issue, self.second_issue])
        self.assertEqual(excepted, response.json()['results'])

