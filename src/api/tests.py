from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from api.models import Projects, CustomUser


class TestCategory(APITestCase):
    url = reverse_lazy('project-list')

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def test_list(self):

        first_user = CustomUser.objects.create(username="Brice", password="123123")
        second_user = CustomUser.objects.create(username="Paul", password="123123")

        first_project = Projects.objects.create(
            title='first_project',
            type='BE',
            author_user_id=first_user,
        )
        second_project = Projects.objects.create(
            title='second_project',
            type='IOS',
            author_user_id=second_user,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'id': project.pk,
                'title': project.title,
                'description': project.description,
                'type': project.type,
                'author_user_id': project.author_user_id.pk
            } for project in [first_project, second_project]
        ]
        self.assertEqual(excepted, response.json())
