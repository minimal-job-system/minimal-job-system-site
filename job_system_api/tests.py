from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.test import TestCase

from job_system_api.models import Job


class ModelTestCase(TestCase):
    """This class defines the test suite for the job model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.job_id = 1
        self.job_name = "Mock Job"
        self.job_type = "test"
        self.job_status = "unknown"
        self.job_meta = {}
        self.job = Job(
            id=self.job_id, name=self.job_name,
            type=self.job_type, status=self.job_status,
            meta=self.job_meta
        )

    def test_model_can_create_a_job(self):
        """Test the job model can create a job."""
        old_count = Job.objects.count()
        self.job.save()
        new_count = Job.objects.count()
        self.assertNotEqual(old_count, new_count)

class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.job_data = {
            'id': 1, 'name': 'Mock Job (1)',
            'type': 'test', 'status': 'unknown',
            'meta': {}
        }
        self.response = self.client.post(
            reverse('create'),
            self.job_data,
            format="json")

    def test_api_can_create_a_job(self):
        """Test the api has job creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_job(self):
        """Test the api can get a given job."""
        job = Job.objects.get()
        response = self.client.get(
            reverse('details',
            kwargs={'pk': job.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, job)

    def test_api_can_update_job(self):
        """Test the api can update a given job."""
        job = Job.objects.get()
        change_job = {
            'name': 'Mock Job (1)',
            'type': 'test', 'status': 'unknown',
            'meta': {}
        }
        res = self.client.put(
            reverse('details', kwargs={'pk': job.id}),
            change_job, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_job(self):
        """Test the api can delete a job."""
        job = Job.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': job.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
