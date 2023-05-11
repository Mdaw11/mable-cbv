from django.urls import reverse
from django.test import TestCase, Client
from .forms import UserRegisterForm
from users.models import CustomUser
from tickets.models import Ticket
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from . decorators import admin_required, developer_required, project_manager_required

# Create your tests here.

class RegisterViewTest(TestCase):
    
    def setUp(self):
        # create a test client and URL for the register view
        self.client = Client()
        self.register_url = reverse('register')
        
        # create a test user for checking if the registration form works correctly
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'account_type': 'admin',
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_register_view_GET(self):
        # test if the register view returns a valid response for GET requests
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)  # check if the response status code is 200
        self.assertTemplateUsed(response, 'users/register.html')  # check if the correct template is used
        self.assertIsInstance(response.context['form'], UserRegisterForm)  # check if the form object is an instance of UserRegisterForm
        
    def test_register_view_POST_valid_form(self):
        # test if the register view creates a new user with valid form data
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'account_type': 'developer',
        }
        response = self.client.post(self.register_url, data=form_data)  # send a POST request with form data
        self.assertEqual(response.status_code, 302)  # check if the response status code is 302 (redirect)
        self.assertRedirects(response, reverse('login'))  # check if the response redirects to the login page
        
        # check if the user has been created with the correct data
        user = CustomUser.objects.get(username=form_data['username'])
        self.assertEqual(user.email, form_data['email'])
        self.assertEqual(user.account_type, form_data['account_type'])
        
    def test_register_view_POST_invalid_form(self):
        # test if the register view handles invalid form data correctly
        form_data = {
            'username': '',
            'email': 'invalidemail',
            'password1': 'password',
            'password2': 'differentpassword',
            'account_type': 'invalid',
        }
        response = self.client.post(self.register_url, data=form_data)  # send a POST request with invalid form data
        self.assertEqual(response.status_code, 200)  # check if the response status code is 200
        self.assertTemplateUsed(response, 'users/register.html')  # check if the correct template is used
        self.assertIsInstance(response.context['form'], UserRegisterForm)  # check if the form object is an instance of UserRegisterForm
        self.assertContains(response, "This field is required.")  # check if the response contains error message for required fields
        self.assertContains(response, "Enter a valid email address.")  # check if the response contains error message for invalid email address
        self.assertContains(response, "The two password fields didn't match.")  # check if the response contains error message for password mismatch
        self.assertContains(response, "Select a valid choice. invalid is not one of the available choices.")  # check if the response contains error message for invalid choice in account_type field
        
        
class ManageUsersViewTest(TestCase):
    
    def setUp(self):
        # create test users and tickets
        self.admin = CustomUser.objects.create_user(username='admin', password='admin', account_type='admin')
        self.developer = CustomUser.objects.create_user(username='dev', password='dev', account_type='developer')
        self.ticket1 = Ticket.objects.create(title='Ticket 1', description='Description 1', created_by=self.admin)
        self.ticket2 = Ticket.objects.create(title='Ticket 2', description='Description 2', created_by=self.developer)
        
        # create a test client and URL for the manage_users view
        self.client = Client()
        self.manage_users_url = reverse('manage-users')
        
    def test_manage_users_view_GET(self):
        # test if the manage_users view returns a valid response for GET requests
        response = self.client.get(self.manage_users_url)
        self.assertEqual(response.status_code, 200)  # check if the response status code is 200
        self.assertTemplateUsed(response, 'users/manage_users.html')  # check if the correct template is used
        
        # check if the tickets are displayed on the page
        self.assertContains(response, self.ticket1.title)
        self.assertContains(response, self.ticket2.title)
        
    def test_manage_users_view_POST(self):
        # test if the manage_users view assigns a ticket to an assignee correctly
        response = self.client.post(self.manage_users_url, {'ticket': self.ticket1.id, 'assignee': self.developer.id})
        self.assertEqual(response.status_code, 302)  # check if the response status code is 302 (redirect)
        self.assertRedirects(response, self.manage_users_url)  # check if the response redirects back to the manage_users page
        
        # check if the assignee of the ticket has been updated correctly
        updated_ticket = Ticket.objects.get(id=self.ticket1.id)
        self.assertEqual(updated_ticket.assignee.first(), self.developer) # check if the ticket has been assigned to the developer
        

class ProfileViewTest(TestCase):
    def setUp(self):
        # create test data for user and tickets
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass'
        )
        self.ticket1 = Ticket.objects.create(
            title='Test Ticket 1', description='Test ticket 1 description', host=self.user
        )
        self.ticket2 = Ticket.objects.create(
            title='Test Ticket 2', description='Test ticket 2 description', assignee=self.user
        )

        self.profile_url = reverse('profile')
        self.login_url = reverse('login')
        
    def test_profile_view_GET(self):
        # test if the profile view returns a 200 OK status code for a logged-in user
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')  # check if the correct template is used
        
        # check if the context data contains the correct tickets
        user_created_tickets = response.context['user_created_tickets']
        user_assigned_tickets = response.context['user_assigned_tickets']
        self.assertEqual(user_created_tickets.count(), 1)  # check if the user has created 1 ticket
        self.assertEqual(user_created_tickets.first(), self.ticket1)  # check if the correct ticket is in the user's created tickets
        self.assertEqual(user_assigned_tickets.count(), 1)  # check if the user has been assigned 1 ticket
        self.assertEqual(user_assigned_tickets.first(), self.ticket2)  # check if the correct ticket is in the user's assigned tickets
        
        # test if the profile view redirects to the login page for an anonymous user
        self.client.logout()
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.profile_url}')  # check if the response redirects to the login page
        
    def test_profile_view_POST(self):
        # test if the profile view updates the user profile information correctly
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.profile_url, {'first_name': 'Test', 'last_name': 'User'})
        self.assertEqual(response.status_code, 302)  # check if the response status code is 302 (redirect)
        self.assertRedirects(response, self.profile_url)  # check if the response redirects back to the profile page
        
        # check if the user profile information has been updated correctly
        updated_user = CustomUser.objects.get(id=self.user.id)
        self.assertEqual(updated_user.first_name, 'Test')  # check if the first name has been updated
        self.assertEqual(updated_user.last_name, 'User')  # check if the last name has been updated
        
def test_admin_required_wrapper_function(self):
    # Create a dummy view function
    def dummy_view_func(request):
        return HttpResponse("Success!")

    # Call the wrapper function with a user that is not an admin
    request = HttpRequest()
    request.user = CustomUser.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password',
        account_type='developer'
    )
    response = admin_required(dummy_view_func)(request)
    self.assertEqual(response.status_code, 403)  # Forbidden response code

    # Call the wrapper function with an admin user
    request.user.account_type = 'admin'
    response = admin_required(dummy_view_func)(request)
    self.assertEqual(response.status_code, 200)  # Success response code
    
def test_manage_users_view_with_admin_required_decorator(self):
    # Create a user that is an admin
    admin_user = CustomUser.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='password',
        account_type='admin'
    )

    # Log in as the admin user
    self.client.force_login(admin_user)

    # Make a GET request to the manage_users view
    response = self.client.get(self.manage_users_url)

    # Check if the response status code is 200 (OK)
    self.assertEqual(response.status_code, 200)

    # Make a POST request to the manage_users view
    response = self.client.post(self.manage_users_url, {'ticket': self.ticket1.id, 'assignee': self.developer.id})

    # Check if the response status code is 302 (redirect)
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, self.manage_users_url)  # check if the response redirects back to the manage_users page

    # Check if the assignee of the ticket has been updated correctly
    updated_ticket = Ticket.objects.get(id=self.ticket1.id)
    self.assertEqual(updated_ticket.assignee, self.developer)
    


class DeveloperRequiredTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.developer = CustomUser.objects.create_user(
            username='developer', email='developer@example.com', password='password'
        )
        
    def test_decorator_with_developer(self):
        # test if the developer_required decorator allows access to a view function for a developer
        self.client.login(username='developer', password='password')
        
        @developer_required
        def test_view(request):
            return HttpResponse('success')
        
        response = test_view(self.client.get(reverse('test_view')))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'success')
        
    def test_decorator_without_developer(self):
        # test if the developer_required decorator denies access to a view function for a non-developer user
        self.client.login(username='user', password='password')
        
        @developer_required
        def test_view(request):
            return HttpResponse('success')
        
        response = test_view(self.client.get(reverse('test_view')))
        self.assertIsInstance(response, HttpResponseForbidden)
        
class ProjectManagerRequiredDecoratorTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.project_manager = CustomUser.objects.create_user(
            username='pm_user',
            email='pm_user@example.com',
            password='pm_password',
            account_type='project_manager'
        )
        self.other_user = CustomUser.objects.create_user(
            username='other_user',
            email='other_user@example.com',
            password='other_password',
            account_type='developer'
        )
        self.test_view_url = reverse('test-view')

    def test_project_manager_can_access_view(self):
        """
        Test that a project manager can access a view that requires project manager permission.
        """
        self.client.login(username='pm_user', password='pm_password')
        response = self.client.get(self.test_view_url)
        self.assertEqual(response.status_code, 200)

    def test_non_project_manager_gets_forbidden(self):
        """
        Test that a non-project manager user gets a forbidden error when trying to access a view
        that requires project manager permission.
        """
        self.client.login(username='other_user', password='other_password')
        response = self.client.get(self.test_view_url)
        self.assertEqual(response.status_code, 403)

    @project_manager_required
    def test_view_that_requires_project_manager_permission(self, request):
        """
        Test view that requires project manager permission.
        """
        return HttpResponse('This is a test view')