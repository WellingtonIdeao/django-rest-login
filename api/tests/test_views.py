from django.test import TestCase
from django.urls import reverse
from django.template.loader import render_to_string
from ..views import UserLoginView, UserLogoutView, UserPasswordChangeView,\
    UserPasswordChangeDoneView, UserPasswordResetView, UserPasswordResetDoneView,\
    UserPasswordResetCompleteView


# coverage run --source='.' manage.py test myapp; coverage report;  coverage html
# python -Wa manage.py test -v 3 --parallel


class UserLoginViewTest(TestCase):
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


class LogoutViewTest(TestCase):
    fixtures = ['user.json']

    def test_logout_url_location(self):
        response = self.client.get('/api/logout/')
        self.assertEqual(response.status_code, 200)

    def test_logout_url_location_by_namespace(self):
        response = self.client.get(reverse('api:logout'))
        self.assertEqual(response.status_code, 200)

    def test_login_template_used_is_correct(self):
        response = self.client.get(reverse('api:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/registration/logged_out.html')

    def test_login_url_name(self):
        response = self.client.get(reverse('api:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.url_name, 'logout')

    def test_login_view_served_the_response(self):
        response = self.client.get(reverse('api:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.view_class, UserLogoutView)

    def test_logout_auth_user(self):
        # login the user
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)

        # logout the user
        response = self.client.get(reverse('api:logout'))
        self.assertEqual(response.status_code, 200)

        # checks if the user is not authenticated
        user_auth = response.context['user'].is_authenticated
        self.assertFalse(user_auth)

    def test_logout_title_is_in_context(self):
        response = self.client.get(reverse('api:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('title' in response.context)


class PasswordChangeViewTest(TestCase):
    fixtures = ['user.json']

    def test_password_change_url_location(self):
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)
        response = self.client.get('/api/password_change/')
        self.assertEqual(response.status_code, 200)

    def test_password_change_url_by_namespace(self):
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('api:password_change'))
        self.assertEqual(response.status_code, 200)

    def test_password_change_template_used_is_correct(self):
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('api:password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/registration/password_change_form.html')

    def test_password_change_redirect_to_login(self):
        response = self.client.get(reverse('api:password_change'), follow=True)
        # last url in redirect chain
        expected_url = response.redirect_chain[-1][0]
        self.assertRedirects(response, expected_url=expected_url)

    def test_password_change_url_name(self):
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)

        response = self.client.get(reverse('api:password_change'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.url_name, 'password_change')

    def test_password_change_view_served_the_response(self):
        response = self.client.get(reverse('api:password_change'))
        self.assertEqual(response.resolver_match.func.view_class, UserPasswordChangeView)

    def test_password_change_title_is_context(self):
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)

        response = self.client.get(reverse('api:password_change'))
        self.assertTrue('title' in response.context)

    def test_password_change_form_is_context(self):
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)

        response = self.client.get(reverse('api:password_change'))
        self.assertTrue('form' in response.context)

    def test_password_change_next_parameter(self):
        response = self.client.get(reverse('api:password_change'))
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, '/api/login/?next=/api/password_change/')

    def test_password_change_success_url(self):
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)
        response = self.client.post(
            reverse('api:password_change'),
            data={
                'old_password': '123456',
                'new_password1': '123%()qwerasd',
                'new_password2': '123%()qwerasd',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse('api:password_change_done'))


class PasswordChangeDoneViewTest(TestCase):
    fixtures = ['user.json']

    def test_password_change_done_url_location(self):
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)
        response = self.client.get('/api/password_change/done/')
        self.assertEqual(response.status_code, 200)

    def test_password_change_done_url_by_namespace(self):
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('api:password_change_done'))
        self.assertEqual(response.status_code, 200)

    def test_password_change_done_template_used_is_correct(self):
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('api:password_change_done'))
        self.assertTemplateUsed(response, 'api/registration/password_change_done.html')

    def test_password_change_done_redirect_to_login(self):
        response = self.client.get(reverse('api:password_change_done'), follow=True)
        # last url in redirect chain
        expected_url = response.redirect_chain[-1][0]
        self.assertRedirects(response, expected_url=expected_url)

    def test_password_change_done_url_name(self):
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)

        response = self.client.get(reverse('api:password_change_done'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.url_name, 'password_change_done')

    def test_password_change_done_view_served_the_response(self):
        response = self.client.get(reverse('api:password_change_done'))
        self.assertEqual(response.resolver_match.func.view_class, UserPasswordChangeDoneView)

    def test_password_change_done_title_is_context(self):
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)

        response = self.client.get(reverse('api:password_change_done'))
        self.assertTrue('title' in response.context)

    def test_password_change_done_next_parameter(self):
        response = self.client.get(reverse('api:password_change_done'))
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, '/api/login/?next=/api/password_change/done/')


class PasswordResetViewTest(TestCase):

    fixtures = ['user.json']

    def test_password_reset_url_location(self):
        response = self.client.get('/api/password_reset/')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_url_by_namespace(self):
        response = self.client.get(reverse('api:password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_template_used_is_correct(self):
        response = self.client.get(reverse('api:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/registration/password_reset_form.html')

    def test_password_reset_url_name(self):
        response = self.client.get(reverse('api:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.url_name, 'password_reset')

    def test_password_reset_view_served_the_response(self):
        response = self.client.get(reverse('api:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.view_class, UserPasswordResetView)

    def test_password_reset_title_is_context(self):
        response = self.client.get(reverse('api:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('title' in response.context)

    def test_password_reset_form_is_context(self):
        response = self.client.get(reverse('api:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)

    def test_password_reset_success_url_non_existent_email(self):
        response = self.client.post(
            reverse('api:password_reset'),
            data={'email': 'test@mail.com'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse('api:password_reset_done'))

    def test_password_reset_success_url_existent_email(self):
        response = self.client.post(
            reverse('api:password_reset'),
            data={'email': 'admin@mail.com'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse('api:password_reset_done'))

    def test_password_reset_send_email_with_success(self):
        from django.core import mail
        response = self.client.post(
            reverse('api:password_reset'),
            data={'email': 'admin@mail.com'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse('api:password_reset_done'))

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

    def test_password_reset_dont_send_email_with_success(self):
        from django.core import mail
        response = self.client.post(
            reverse('api:password_reset'),
            data={'email': 'test@mail.com'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse('api:password_reset_done'))

        # Test that no one message has been sent.
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_subject_template_name(self):
        from django.core import mail
        response = self.client.post(
            reverse('api:password_reset'),
            data={'email': 'admin@mail.com'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse('api:password_reset_done'))

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        subject_template_name = 'api/registration/password_reset_subject.txt'
        context = {'email': 'admin@mail.com'}

        # Load a template and render it with a context. Return a string.
        subject = render_to_string(subject_template_name, context)

        # # Email subject *must not* contain newlines. Remove them
        subject = ''.join(subject.splitlines())

        # Test that one message has been sent, it has a subject
        self.assertEqual(mail.outbox[0].subject, subject)


class PasswordResetDoneViewTest(TestCase):

    def test_password_reset_done_url_location(self):
        response = self.client.get('/api/password_reset/done/')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_url_by_namespace(self):
        response = self.client.get(reverse('api:password_reset_done'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_template_used_is_correct(self):
        response = self.client.get(reverse('api:password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/registration/password_reset_done.html')

    def test_password_reset_done_url_name(self):
        response = self.client.get(reverse('api:password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.url_name, 'password_reset_done')

    def test_password_reset_done_title_is_context(self):
        response = self.client.get(reverse('api:password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('title' in response.context)

    def test_password_reset_view_served_the_response(self):
        response = self.client.get(reverse('api:password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.view_class, UserPasswordResetDoneView)


class PasswordResetCompleteViewTest(TestCase):

    def test_password_reset_complete_url_location(self):
        response = self.client.get('/api/reset/done/')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_url_by_namespace(self):
        response = self.client.get(reverse('api:password_reset_complete'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_template_used_is_correct(self):
        response = self.client.get(reverse('api:password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/registration/password_reset_complete.html')

    def test_password_reset_complete_url_name(self):
        response = self.client.get(reverse('api:password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.url_name, 'password_reset_complete')

    def test_password_reset_complete_title_is_context(self):
        response = self.client.get(reverse('api:password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('title' in response.context)

    def test_password_reset_complete_view_served_the_response(self):
        response = self.client.get(reverse('api:password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.view_class, UserPasswordResetCompleteView)














