from unittest.mock import MagicMock, Mock, patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from common.const import WEBSITE_STATUSES
import common.fixtures.test_fixtures as test_fixtures
from .models import Website


class BaseAPITestCase(APITestCase):
    """
    Base class for all api.
    We can ganerate some fake data here or other extra functions that can be a base for other tests.
    """
    def setUp(self):
        super(BaseAPITestCase, self).setUp()


class TestWebsite(BaseAPITestCase):

    endpoint_url = reverse('website:list')
    website_url = 'https://en.wikipedia.org/wiki/List_of_game_engines'

    def test_website_process_fail_url(self):
        payload = {
            'website_url': 'wrong website url',
        }
        response = self.client.post(self.endpoint_url, data=payload)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertEqual(
            response.data['website_url'][0].code,
            'invalid'
        )
        self.assertEqual(
            response.data['website_url'][0].title(),
            'Enter A Valid Url.'
        )

    @patch("requests.get")
    def test_website_process_started_with_task_fail(self, mock_requests_get):
        mock_requests_get.return_value = Mock(ok=False)

        # endpoint_url = reverse('website:list', kwargs={'eoi_id': eoi.pk})

        payload = {
            'website_url': self.website_url,
        }
        response = self.client.post(self.endpoint_url, data=payload)

        self.assertTrue(status.is_success(response.status_code),
                        "We exect to have post with success.")
        self.assertEqual(response.data['status'],
                         WEBSITE_STATUSES[WEBSITE_STATUSES.started],
                         "System should start processing the website.")

        website = Website.objects.get(pk=response.data['id'])
        self.assertEqual(response.data['hostname'],
                         website.hostname)
        self.assertEqual(response.data['uri'],
                         website.uri)
        # because of CELERY_TASK_ALWAYS_EAGER = True in settings we run task sync
        # we expect to fail on request.get.. so the process should fail
        self.assertEqual(website.get_status(), WEBSITE_STATUSES[WEBSITE_STATUSES.failed])

    @patch("requests.get")
    @patch("website_process.tasks.get_image_from_response")
    def test_website_process_started_with_task_success(
            self, mock_get_image_from_response, mock_requests_get):
        mock_get_image_from_response.side_effect = [
            test_fixtures.wiki_btn_image(),
            test_fixtures.wiki_btn_image(),
            test_fixtures.wiki_btn_image(),
        ]
        mock_requests_get.side_effect = [
            MagicMock(ok=True, text=test_fixtures.html_wiki_example_game_engines()),
            MagicMock(ok=True, status_code=200),
            MagicMock(ok=True, status_code=200),
            MagicMock(ok=True, status_code=200),
        ]
        payload = {
            'website_url': self.website_url,
        }
        response = self.client.post(self.endpoint_url, data=payload)
        self.assertTrue(status.is_success(response.status_code),
                        "We exect to have post with success.")
        self.assertTrue(response.data['text'])

        website = Website.objects.get(pk=response.data['id'])
        self.assertEqual(website.images_count, 3)
        self.assertEqual(
            website.get_status(),
            WEBSITE_STATUSES[WEBSITE_STATUSES.success],
            "We expect success, because of CELERY_TASK_ALWAYS_EAGER is True in settings. "
            "Task in that configuration will run synchronously."
        )
