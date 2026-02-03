from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import MissingRequest


class AdminBadgeTest(TestCase):
    def setUp(self):
        User = get_user_model()
        # create staff user for admin url reversing if needed
        self.admin = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        # create a normal student user
        self.student = User.objects.create_user('student', 's@example.com', 'password')

    def test_unhandled_missing_count_tag(self):
        # initially zero
        self.assertEqual(MissingRequest.objects.filter(handled_at__isnull=True).count(), 0)
        # create two missing requests
        MissingRequest.objects.create(student=self.student, title='T1', authors='A', justification='J')
        MissingRequest.objects.create(student=self.student, title='T2', authors='A', justification='J')
        self.assertEqual(MissingRequest.objects.filter(handled_at__isnull=True).count(), 2)
        # mark one as handled
        mr = MissingRequest.objects.first()
        mr.handled_at = None
        # still unhandled
        self.assertEqual(MissingRequest.objects.filter(handled_at__isnull=True).count(), 2)
