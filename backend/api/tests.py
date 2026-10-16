from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Ticket, Reply

class HelpDeskAPITests(APITestCase):

    def setUp(self):
        # Test uchun foydalanuvchi yaratamiz
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')
        self.tickets_url = reverse('ticket-list-create')
        self.replies_url = reverse('reply-create')

    def test_register_user(self):
        """Foydalanuvchini ro'yxatdan o'tkazish testi"""
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'new@example.com'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user_returns_token(self):
        """Login qilganda token va username qaytarish testi"""
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('username', response.data)

    def test_create_ticket_authenticated(self):
        """Autentifikatsiyadan o'tib tiket yaratish va validatsiya testi"""
        # Avval token olamiz
        login_res = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        token = login_res.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Yaroqli tiket yaratish
        ticket_data = {'title': 'Test Ticket', 'description': 'Test Description'}
        response = self.client.post(self.tickets_url, ticket_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ticket_validation_error(self):
        """Bo'sh sarlavha kiritilganda validatsiya xatosi qaytarish testi"""
        login_res = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        token = login_res.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Bo'sh sarlavha berilganda HTTP 400 Bad Request qaytishi kerak
        response = self.client.post(self.tickets_url, {'title': '', 'description': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)