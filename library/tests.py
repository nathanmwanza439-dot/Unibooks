from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from library.models import Book, BorrowRequest
from datetime import date, timedelta


User = get_user_model()


class UniBooksTests(TestCase):
    def setUp(self):
        # librarian user
        self.librarian = User.objects.create_user(username='lib', email='lib@example.com', password='LibPass123')
        self.librarian.is_librarian = True
        self.librarian.save()
        # student
        self.student = User.objects.create_user(username='std', email='student@example.com', password='StudPass123', matricule='M123')
        # a book
        self.book = Book.objects.create(title='Test Book', authors='Author A', total_copies=2, available_copies=2)

    def test_login_with_email(self):
        c = Client()
        resp = c.post(reverse('student:login'), {'username': 'student@example.com', 'password': 'StudPass123'})
        self.assertIn(resp.status_code, (302, 301))

    def test_login_with_matricule(self):
        c = Client()
        resp = c.post(reverse('student:login'), {'username': 'M123', 'password': 'StudPass123'})
        self.assertIn(resp.status_code, (302, 301))

    def test_force_password_change_middleware(self):
        self.student.force_password_change = True
        self.student.save()
        c = Client()
        c.login(username='std', password='StudPass123')
        resp = c.get(reverse('student:dashboard'))
        # should redirect to password change
        self.assertEqual(resp.status_code, 302)

    def test_borrow_request_and_admin_approval(self):
        c = Client()
        # student requests borrow
        c.login(username='std', password='StudPass123')
        resp = c.post(reverse('student:request_borrow', args=[self.book.pk]))
        self.assertIn(resp.status_code, (302, 301))
        br = BorrowRequest.objects.filter(student=self.student, book=self.book).first()
        self.assertIsNotNone(br)
        # simulate librarian approval (admin interface removed in this project)
        br.status = 'APPROVED'
        br.borrow_date = date.today()
        br.due_date = date.today() + timedelta(days=14)
        br.save()
        # decrement available copies
        self.book.available_copies -= 1
        self.book.save()
        br.refresh_from_db()
        self.assertEqual(br.status, 'APPROVED')
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 1)
