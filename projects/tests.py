from django.test import TestCase, Client
from django.urls import reverse
from projects.models import Project
from tickets.models import Ticket
from users.models import CustomUser
from projects.forms import ProjectForm

# Create your tests here.

class ProjectHomeViewTest(TestCase):
    
    def setUp(self):
        # Create a test client and set the URL to the project home page
        self.client = Client()
        self.url = reverse('project_home')
        
        # Create some test projects to use in the tests
        self.project1 = Project.objects.create(name='Project 1', description='Description 1')
        self.project2 = Project.objects.create(name='Project 2', description='Description 2')
        self.project3 = Project.objects.create(name='Project 3', description='Description 3')
        
    def test_project_home_view_with_no_search_query(self):
        # Test the project home page with no search query
        
        # Send a GET request to the project home page
        response = self.client.get(self.url)
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct template was used to render the response
        self.assertTemplateUsed(response, 'projects/project_home.html')
        
        # Check that the list of projects in the response context is equal to the list of test projects
        self.assertQuerysetEqual(
            response.context['projects'],
            ['<Project: Project 1>', '<Project: Project 2>', '<Project: Project 3>']
        )
        
    def test_project_home_view_with_search_query(self):
        # Test the project home page with a search query
        
        # Send a GET request to the project home page with a search query parameter
        response = self.client.get(self.url, {'search': '1'})
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct template was used to render the response
        self.assertTemplateUsed(response, 'projects/project_home.html')
        
        # Check that the list of projects in the response context contains only the test project with '1' in its name or description
        self.assertQuerysetEqual(
            response.context['projects'],
            ['<Project: Project 1>']
        )
        

class ProjectViewTest(TestCase):
    def setUp(self):
        # Create a client for making requests
        self.client = Client()
        
        # Create a project for testing
        self.project = Project.objects.create(
            name='Test Project',
            description='This is a test project.'
        )
        
        # Create tickets for the project
        self.ticket1 = Ticket.objects.create(
            project=self.project,
            name='Test Ticket 1',
            description='This is a test ticket 1.',
            assignee=self.project.manager,
            status='To Do',
            priority='Low',
            type='Bug'
        )
        self.ticket2 = Ticket.objects.create(
            project=self.project,
            name='Test Ticket 2',
            description='This is a test ticket 2.',
            assignee=self.project.manager,
            status='In Progress',
            priority='High',
            type='Feature'
        )
    
    def test_project_view_with_no_search_query(self):
        # Make a GET request to the project view with no search query
        response = self.client.get(reverse('project', args=[self.project.id]))
        
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Assert that the correct template is used to render the response
        self.assertTemplateUsed(response, 'projects/project.html')
        
        # Assert that the projects object in the response context contains the correct project
        self.assertEqual(response.context['projects'], self.project)
        
        # Assert that the tickets object in the response context contains the correct ticket
        self.assertQuerysetEqual(
            response.context['tickets'],
            [repr(self.ticket1), repr(self.ticket2)],
            ordered=False
        )
    
    def test_project_view_with_search_query(self):
        # Make a GET request to the project view with a search query
        response = self.client.get(reverse('project', args=[self.project.id]), {'search': 'ticket 1'})
        
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Assert that the correct template is used to render the response
        self.assertTemplateUsed(response, 'projects/project.html')
        
        # Assert that the projects object in the response context contains the correct project
        self.assertEqual(response.context['projects'], self.project)
        
        # Assert that the tickets object in the response context contains the correct tickets
        self.assertQuerysetEqual(
            response.context['tickets'],
            [repr(self.tickets1)],
            ordered=False
        )
        
class CreateProjectViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create-project')
        self.user = CustomUser.objects.create_user(
            username='testuser', password='testpass'
        )
    
    def test_create_project_view_with_valid_form_submission(self):
        # Login the user
        self.client.login(username='testuser', password='testpass')
        
        # Create a dictionary of form data
        form_data = {'name': 'New Project', 'description': 'New Project Description'}
        
        # Post the form to the view
        response = self.client.post(self.url, data=form_data)
        
        # Check if the view redirected to the project home page
        self.assertRedirects(response, reverse('project-home'))
        
        # Check if the new project was added to the database
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.name, 'New Project')
        self.assertEqual(project.description, 'New Project Description')
        
    def test_create_project_view_with_invalid_form_submission(self):
        # Login the user
        self.client.login(username='testuser', password='testpass')
        
        # Create a dictionary of invalid form data
        form_data = {'name': '', 'description': ''}
        
        # Post the form to the view
        response = self.client.post(self.url, data=form_data)
        
        # Check if the view returned a 200 status code
        self.assertEqual(response.status_code, 200)
        
        # Check if the form was not saved to the database
        self.assertEqual(Project.objects.count(), 0)
        
        # Check if the form contains error messages
        form = response.context['form']
        self.assertTrue(form.errors)
        
class UpdateProjectViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(name='Test Project', description='Test Description')
        self.url = reverse('update-project', args=[self.project.id])
    
    # Test the update project view with GET request
    def test_update_project_view_with_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_form.html')
        self.assertIsInstance(response.context['form'], ProjectForm)
        self.assertEqual(response.context['project'], self.project)

    # Test the update project view with valid POST request
    def test_update_project_view_with_valid_post_request(self):
        data = {'name': 'Updated Name', 'description': 'Updated Description'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('project', args=[self.project.id]))
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Updated Name')
        self.assertEqual(self.project.description, 'Updated Description')

    # Test the update project view with invalid POST request
    def test_update_project_view_with_invalid_post_request(self):
        data = {'name': '', 'description': ''}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_form.html')
        self.assertIsInstance(response.context['form'], ProjectForm)
        self.assertEqual(response.context['project'], self.project)
        
class UpdateProjectIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(name='Test Project', description='Test Description')
        self.url = reverse('update-project', args=[self.project.id])
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
    
    def test_update_project_view_integration(self):
    # Test valid post request
        data = {'name': 'Updated Name', 'description': 'Updated Description'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('project', args=[self.project.id]))
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Updated Name')
        self.assertEqual(self.project.description, 'Updated Description')

    # Test invalid post request
        data = {'name': '', 'description': ''}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_form.html')
        self.assertIsInstance(response.context['form'], ProjectForm)
        self.assertEqual(response.context['project'], self.project)
        
class DeleteProjectViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(name='Test Project', description='Test Description')
        self.url = reverse('delete-project', args=[self.project.id])

    def test_delete_project_view_with_get_request(self):
        # Test that the delete project page is displayed when using a GET request
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project-delete.html')
        self.assertEqual(response.context['obj'], self.project)

    def test_delete_project_view_with_post_request(self):
        # Test that a project can be deleted with a valid POST request
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('project-home'))
        with self.assertRaises(Project.DoesNotExist):
            Project.objects.get(id=self.project.id)

    def test_delete_project_view_with_invalid_post_request(self):
        # Test that a project is not deleted with an invalid POST request
        url = reverse('delete-project', args=[10000])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

class DeleteProjectIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(name='Test Project', description='Test Description')
        self.url = reverse('delete-project', args=[self.project.id])
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
    
    def test_delete_project_view_integration(self):
        # Test that a project can be deleted with a valid POST request while logged in
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('project-home'))
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

        # Test that a project is not deleted with an invalid POST request while logged in
        url = reverse('delete-project', args=[10000])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)