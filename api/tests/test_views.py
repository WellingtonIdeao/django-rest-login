from django.test import TestCase
from django.urls import reverse
from ..views import UserLoginView

# coverage run --source='.' manage.py test myapp; coverage report;  coverage html
# python -Wa manage.py test -v 3 --parallel


class UserLoginViewTestCase(TestCase):
    fixtures = ['user.json']

    def test_login_url_location(self):
        response = self.client.get('/api/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_url_location_by_namespace(self):
        response = self.client.get(reverse('api:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_template_used_is_correct(self):
        response = self.client.get(reverse('api:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/registration/login.html')

    def test_login_url_name(self):
        response = self.client.get(reverse('api:login'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.url_name, 'login')

    def test_login_view_served_the_response(self):
        response = self.client.get(reverse('api:login'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.view_class, UserLoginView)

    def test_logging_a_user_was_successful(self):
        # logged_in is True if the credentials were accepted and login was successful.
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('api:login'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'admin')

    def test_redirect_to_correct_page_after_login(self):
        response = self.client.post(reverse('api:login'), data={'username': 'admin', 'password': '123456'}, follow=True)
        self.assertEqual(response.status_code, 200)
        # checks if redirect to correct page after the user logged in.
        self.assertRedirects(response, expected_url=reverse('admin:index'))

    def test_form_is_in_context(self):
        response = self.client.get(reverse('api:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)

    def test_user_is_not_authenticated(self):
        response = self.client.get(reverse('api:login'))
        self.assertEqual(response.status_code, 200)
        user = response.context['user']
        is_auth = user.is_authenticated
        self.assertFalse(is_auth)








