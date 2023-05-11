from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tickets.models import Ticket, Message, Attachment, Category, CustomUser
from projects.models import Project
from tickets.forms import TicketForm

# Create your tests here.

class TicketDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.ticket = Ticket.objects.create(title='Test Ticket', creator=self.user)

    def test_correct_messages_displayed(self):
        # Add some messages to the ticket
        Message.objects.create(user=self.user, ticket=self.ticket, body='Message 1')
        Message.objects.create(user=self.user, ticket=self.ticket, body='Message 2')
        Message.objects.create(user=self.user, ticket=self.ticket, body='Message 3')
        
        # Make a GET request to the ticket detail page
        response = self.client.get(reverse('ticket', args=[self.ticket.id]))

        # Check that the correct messages are displayed
        self.assertContains(response, 'Message 1')
        self.assertContains(response, 'Message 2')
        self.assertContains(response, 'Message 3')

    def test_correct_search_results_displayed(self):
        # Add some messages to the ticket
        Message.objects.create(user=self.user, ticket=self.ticket, body='Search Term')
        Message.objects.create(user=self.user, ticket=self.ticket, body='Not Found')
        
        # Make a GET request with a search query
        response = self.client.get(reverse('ticket', args=[self.ticket.id]) + '?q=Search')

        # Check that only the matching message is displayed
        self.assertContains(response, 'Search Term')
        self.assertNotContains(response, 'Not Found')

    def test_correct_number_of_objects_per_page(self):
        # Add some messages to the ticket
        for i in range(10):
            Message.objects.create(user=self.user, ticket=self.ticket, body=f'Message {i}')
        
        # Make a GET request to the ticket detail page with a page number
        response = self.client.get(reverse('ticket', args=[self.ticket.id]) + '?messages_page=2')

        # Check that only the correct number of messages are displayed
        self.assertContains(response, 'Message 5')
        self.assertContains(response, 'Message 6')
        self.assertContains(response, 'Message 7')
        self.assertContains(response, 'Message 8')
        self.assertContains(response, 'Message 9')
        self.assertNotContains(response, 'Message 0')
        self.assertNotContains(response, 'Message 1')
        self.assertNotContains(response, 'Message 2')
        self.assertNotContains(response, 'Message 3')
        self.assertNotContains(response, 'Message 4')

    def test_invalid_page_number_raises_error(self):
        # Make a GET request with an invalid page number
        response = self.client.get(reverse('ticket', args=[self.ticket.id]) + '?messages_page=foo')

        # Check that a 404 error is raised
        self.assertEqual(response.status_code, 404)

    def test_message_created_with_post_request(self):
        # Log in as the test user
        self.client.login(username='testuser', password='testpass')

        # Make a POST request with a message body
        response = self.client.post(reverse('ticket', args=[self.ticket.id]), {'body': 'New Message'})

        # Check that a new message was created and added to the ticket
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().body, 'New Message')
        self.assertEqual(self.ticket.participants.count(), 1)
        self.assertEqual(self.ticket.participants.first(),)
        

class CreateTicketTest(TestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        
        # Create a test project
        self.project = Project.objects.create(
            name='Test Project',
            description='A test project'
        )
        
        # Create some test categories
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')
        
        # Create some test users
        self.user1 = CustomUser.objects.create(username='User 1')
        self.user2 = CustomUser.objects.create(username='User 2')
        
    def test_create_ticket(self):
        # Login as the test user
        self.client.login(username='testuser', password='testpass')
        
        # Make a POST request to create a new ticket
        response = self.client.post(reverse('create_ticket'), {
            'name': 'Test Ticket',
            'description': 'A test ticket',
            'status': 'Open',
            'priority': 'Low',
            'type': 'Bug',
            'project': self.project.id,
            'category': self.category1.name,
            'assignee': [self.user1.id, self.user2.id]
        })
        
        # Assert that the ticket was created successfully and redirected to the ticket detail page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('ticket', args=[1]))
        
        # Assert that the ticket was created with the correct information
        ticket = Ticket.objects.get(id=1)
        self.assertEqual(ticket.name, 'Test Ticket')
        self.assertEqual(ticket.description, 'A test ticket')
        self.assertEqual(ticket.status, 'Open')
        self.assertEqual(ticket.priority, 'Low')
        self.assertEqual(ticket.type, 'Bug')
        self.assertEqual(ticket.project, self.project)
        self.assertEqual(ticket.category, self.category1)
        self.assertCountEqual(ticket.assignee.all(), [self.user1, self.user2])
        
        # Assert that the ticket was not created with incorrect information
        self.assertNotEqual(ticket.name, 'Wrong Ticket Name')
        self.assertNotEqual(ticket.description, 'Wrong Ticket Description')
        self.assertNotEqual(ticket.status, 'Closed')
        self.assertNotEqual(ticket.priority, 'High')
        self.assertNotEqual(ticket.type, 'Feature')
        self.assertNotEqual(ticket.project, None)
        self.assertNotEqual(ticket.category, self.category2)
        self.assertCountEqual(ticket.assignee.all(), [self.user1, self.user2])
        

class UpdateTicketViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a test user and log them in
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Create a test category
        self.category = Category.objects.create(name='Test Category')
        
        # Create a test ticket
        self.ticket = Ticket.objects.create(
            name='Test Ticket',
            host=self.user,
            category=self.category,
            status='open',
            priority='high',
            type='bug',
            description='This is a test ticket.'
        )
    
def test_update_ticket_view(self):
    # Define the URL for the update ticket view with the ticket id
    url = reverse('update-ticket', args=[self.ticket.id])
    
    # Make a GET request to the update ticket view URL
    response = self.client.get(url)
    
    # Assert that the response status code is 200
    self.assertEqual(response.status_code, 200)
    
    # Assert that the response contains the ticket name
    self.assertContains(response, self.ticket.name)
    
    # Assert that the response contains the ticket category name
    self.assertContains(response, self.ticket.category.name)
    
    # Assert that the response contains the ticket status
    self.assertContains(response, self.ticket.status)
    
    # Assert that the response contains the ticket priority
    self.assertContains(response, self.ticket.priority)
    
    # Assert that the response contains the ticket type
    self.assertContains(response, self.ticket.type)
    
    # Assert that the response contains the ticket description
    self.assertContains(response, self.ticket.description)
    
    # Define the data for the POST request to update the ticket
    data = {
        'name': 'Updated Test Ticket',
        'category': 'New Test Category',
        'status': 'closed',
        'priority': 'medium',
        'type': 'feature',
        'description': 'This is an updated test ticket.',
    }
    
    # Make a POST request to the update ticket view URL with the updated data
    response = self.client.post(url, data=data)
    
    # Assert that the response status code is 302 (redirect)
    self.assertEqual(response.status_code, 302)
    
    # Assert that the ticket name was updated
    self.ticket.refresh_from_db()
    self.assertEqual(self.ticket.name, 'Updated Test Ticket')
    
    # Assert that the ticket category was updated
    self.assertEqual(self.ticket.category.name, 'New Test Category')
    
    # Assert that the ticket status was updated
    self.assertEqual(self.ticket.status, 'closed')
    
    # Assert that the ticket priority was updated
    self.assertEqual(self.ticket.priority, 'medium')
    
    # Assert that the ticket type was updated
    self.assertEqual(self.ticket.type, 'feature')
    
    # Assert that the ticket description was updated
    self.assertEqual(self.ticket.description, 'This is an updated test ticket.')
    

def test_delete_ticket_view(self):
    # Create a user for the test
    user = CustomUser.objects.create_user(
    username='testuser', password='testpass')
    user.save()
    # Create a ticket for the test
    ticket = Ticket.objects.create(
        host=user,
        category=self.category,
        project=self.project,
        name='Test Ticket',
        status='Open',
        priority='High',
        type='Task',
        description='This is a test ticket.'
    )

    # Login the user
    self.client.login(username='testuser', password='testpass')

    # Make a POST request to delete the ticket
    response = self.client.post(reverse('delete-ticket', args=[ticket.id]))

    # Check if the ticket has been deleted
    self.assertEqual(response.status_code, 302)
    self.assertFalse(Ticket.objects.filter(id=ticket.id).exists())
    
def test_delete_message_view(self):
    # Create a user for the test
    user = CustomUser.objects.create_user(
    username='testuser', password='testpass')
    user.save()
    
    # Create a ticket for the test
    ticket = Ticket.objects.create(
        host=user,
        category=self.category,
        project=self.project,
        name='Test Ticket',
        status='Open',
        priority='High',
        type='Task',
        description='This is a test ticket.'
    )

    # Create a message for the test
    message = Message.objects.create(
        ticket=ticket,
        user=user,
        content='This is a test message.'
    )

    # Login the user
    self.client.login(username='testuser', password='testpass')

    # Make a POST request to delete the message
    response = self.client.post(reverse('delete-message', args=[message.id]))

    # Check if the message has been deleted
    self.assertEqual(response.status_code, 302)
    self.assertFalse(Message.objects.filter(id=message.id).exists())