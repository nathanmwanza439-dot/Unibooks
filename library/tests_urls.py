from django.test import TestCase, Client
from django.test.utils import override_settings


@override_settings(ALLOWED_HOSTS=['localhost', 'testserver'])
class LegacyStudentUrlsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_legacy_student_urls_render_landing(self):
        paths = [
            '/student/login/',
            '/student/dashboard/',
            '/student/password_change/',
            '/student/subscription_required/',
        ]
        for p in paths:
            with self.subTest(path=p):
                resp = self.client.get(p, HTTP_HOST='localhost')
                self.assertEqual(resp.status_code, 200)
                self.assertContains(resp, 'Page déplacée')
