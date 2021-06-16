from django.test import Client
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class RegisterTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_page_status_code(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/register.html')

    def test_register_user_fail(self):
        # The registration data is invalid. First name contains a digits.
        user_data = {
            'username': 'testuser',
            'first_name': 'firstname1111',
            'last_name': 'lastname',
            'email': 'testemail@gmail.com',
            'birth_date': '2020-12-07',
            'gender': 'M',
            'password1': 'testpass1',
            'password2': 'testpass1',
        }

        response = self.client.post(reverse('register'), user_data)
        self.assertEqual(response.status_code, 200)

        # Since the data is not valid and the user is not registered, a db is empty.
        self.assertEqual(Profile.objects.count(), 0)

    def test_register_user_success(self):
        # The registration data is valid.
        user_data = {
            'username': 'testuser',
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'testemail@gmail.com',
            'birth_date': '2020-12-07',
            'gender': 'M',
            'password1': 'testpass1',
            'password2': 'testpass1',
        }

        response = self.client.post(reverse('register'), user_data)
        self.assertEqual(response.status_code, 200)

        # The user has been registered and added to the db.
        self.assertEqual(Profile.objects.count(), 1)


class UserProfileTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = Profile.objects.create(
            username='testuser',
            first_name='firstname',
            last_name='lastname',
            email='testemail@gmail.com',
            birth_date='2020-12-07',
            gender='M',
        )

    def test_login_page_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/login.html')

    def test_login_user_success(self):
        self.user.set_password('testpass1')
        self.user.save()
        self.user.is_active = True

        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass1'})
        self.assertEqual(response.status_code, 302)

    def test_login_user_fail(self):
        self.user.set_password('testpass1')
        self.user.save()
        self.user.is_active = True

        # Login data is invalid. Incorrect password.
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass22'})
        self.assertEqual(response.status_code, 200)

    def test_profile_page_status_code(self):
        # User successfully login.
        self.test_login_user_success()

        # Get profile page.
        profile_response = self.client.get(reverse('user_profile'))
        self.assertEqual(profile_response.status_code, 200)

    def test_logout_user(self):
        logout_response = self.client.get(reverse('logout'))
        self.assertEqual(logout_response.status_code, 302)

    def test_edit_user_profile(self):
        self.test_login_user_success()

        # Check that the user does not have a phone number.
        self.assertEqual(self.user.phone, '')

        # Update the user phone number and last name.
        edit_response = self.client.post(reverse('edit_profile'),
                                         {
                                             'username': 'testuser',
                                             'first_name': 'firstname',
                                             'last_name': 'newlastname',
                                             'email': 'testemail@gmail.com',
                                             'birth_date': '2020-12-07',
                                             'gender': 'M',
                                             'phone': '+375297777777',
                                         }
                                         )
        self.assertEqual(edit_response.status_code, 200)

        # Refresh db with new data.
        self.user.refresh_from_db()

        # Check that the data in the db has been updated.
        self.assertEqual(self.user.phone, '+375297777777')
        self.assertEqual(self.user.last_name, 'newlastname')

    def test_remove_user_account(self):
        self.test_login_user_success()

        # Get remove_account page.
        remove_account_response = self.client.get(reverse('remove_account'))
        self.assertEqual(remove_account_response.status_code, 200)

        # Now there is only one account in the db
        self.assertEqual(Profile.objects.count(), 1)

        # Remove user account
        remove_account_response = self.client.post(reverse('remove_account'))
        self.assertEqual(remove_account_response.status_code, 200)

        # The db is empty after removing the user account
        self.assertEqual(Profile.objects.count(), 0)
