from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.paginator import Paginator
from django.views import View
from .models import Ticket, TicketHistory, Attachment, Category, Message
from .forms import TicketForm
from .filters import TicketFilter
from projects.models import Project
from users.models import CustomUser



# Create your views here.
class HomeView(View):
    def get(self, request):
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        
        tickets = Ticket.objects.all()
        # Get all projects created by or assigned to user
        user = request.user
        projects = Project.objects.filter(
            Q(user=request.user) |
            Q(assigned_users=user) | 
            Q(project__assignee=user)
        ).distinct()
        
        if q:
            tickets = Ticket.objects.filter(
                Q(category__name__icontains=q) |
                Q(name__icontains=q) |
                Q(description__icontains=q)
            )
            
        # Get count of all tickets
        ticket_count = tickets.count()
        
        # Get count of completed tickets
        completed_ticket_count = tickets.filter(status=False).count()
        
        # Get count of all projects
        project_count = projects.count()
        
        # Get count of completed projects
        completed_project_count = projects.filter(status='Done').count()
        
        paginator = Paginator(projects, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'tickets': tickets,
                   'ticket_count': ticket_count,
                   'projects': projects,
                   'project_count': project_count,
                   'page_obj': page_obj,
                   'completed': completed_project_count + completed_ticket_count,
        }

        return render(request, 'dashboard/dashboard.html', context)

class AnalyticsView(View):
    def get(self, request):
        
        return render(request, 'dashboard/analytics.html')

def get_ticket_data(request):
    high_priority = Ticket.objects.filter(priority='High').count()
    medium_priority = Ticket.objects.filter(priority='Medium').count()
    low_priority = Ticket.objects.filter(priority='Low').count()
    none_priority = Ticket.objects.filter(priority='None').count()
    
    data = {
        'values': [high_priority, medium_priority, low_priority, none_priority]
    }
    
    return JsonResponse(data)


def get_type_data(request):
    misc_type = Ticket.objects.filter(type='Misc').count()
    bug_type = Ticket.objects.filter(type='Bug').count()
    help_type = Ticket.objects.filter(type='Help Needed').count()
    concern_type = Ticket.objects.filter(type='Concern').count()
    question_type = Ticket.objects.filter(type='Question').count()
    
    data = {
        'values': [misc_type, bug_type, help_type, concern_type, question_type]
    }
    
    return JsonResponse(data)

def get_status_data(request):
    open_status = Ticket.objects.filter(status='Open').count()
    close_status = Ticket.objects.filter(status='Closed').count()
    
    data = {
        'values': [open_status, close_status]
    }
    
    return JsonResponse(data)

class TicketHomeView(View):
    def get(self, request):
        tickets = Ticket.objects.filter(
            Q(host=request.user) |
            Q(assignee=request.user)
        )
        search_query = request.GET.get('search')
        
        # Apply filters based on GET parameters
        filterset = TicketFilter(request.GET, queryset=tickets)
        tickets = filterset.qs
        
        # Filter tickets based on a search query
        if search_query:
            tickets = tickets.filter(
                Q(host__username__icontains=search_query) |
                Q(assignee__username__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(status__icontains=search_query) |
                Q(priority__icontains=search_query) |
                Q(type__icontains=search_query)
            )
            
        # Paginate the ticket table
        paginator = Paginator(tickets, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        categories = Category.objects.all()[0:5]
        ticket_count = tickets.count()
        
        

        if request.user.is_authenticated:
            user = request.user
            tickets = tickets.filter(Q(host=user) | Q(assignee=user))

        

        context = {'tickets': tickets, 'categories': categories,
                   'ticket_count': ticket_count, 'page_obj': page_obj,
                   'search_query': search_query, 'filter': filterset}
        
        return render(request, 'tickets/ticket_home.html', context)


# Ticket detail page
class TicketView(View):
    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, id=pk)
        ticket_messages = ticket.message_set.all()
        ticket_history = ticket.history.all()
        ticket_attachments = ticket.attachments.all()
        
        # Get the search query from the request's GET parameters
        search_query = request.GET.get('q')
        
        # Filter the results based on the search query
        if search_query:
            ticket_messages = ticket_messages.filter(Q(user__username__icontains=search_query) | 
                                                     Q(body__icontains=search_query))
            
            ticket_history = ticket_history.filter(Q(name__icontains=search_query) |
                                                   Q(description__icontains=search_query) |
                                                   Q(updated_by__username__icontains=search_query))
            
            ticket_attachments = ticket_attachments.filter(Q(file__icontains=search_query) |
                                                    Q(created__icontains=search_query))
        
        # Set the number of items you want to display on each page
        messages_per_page = 5
        history_per_page = 5
        attachments_per_page = 5
        
        # Create a paginator object for each queryset
        messages_paginator = Paginator(ticket_messages, messages_per_page)
        history_paginator = Paginator(ticket_history, history_per_page)
        attachments_paginator = Paginator(ticket_attachments, attachments_per_page)
    
        # Get the current page number from the request's GET parameters 
        messages_page_number = request.GET.get('messages_page')
        history_page_number = request.GET.get('history_page')
        attachments_page_number = request.GET.get('attachments_page')
    
        # Get the current page object for each queryset
        messages_page_obj = messages_paginator.get_page(messages_page_number)
        history_page_obj = history_paginator.get_page(history_page_number)
        attachments_page_obj = attachments_paginator.get_page(attachments_page_number)
        
        
        context = {
            'ticket': ticket, 
            'ticket_messages': messages_page_obj, 
            'ticket_history': history_page_obj,
            'ticket_attachments': attachments_page_obj,
            'search_query': search_query,
        }
        return render(request, 'tickets/ticket.html', context)

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, id=pk)
        ticket_messages = ticket.message_set.all()
        ticket_history = ticket.history.all()
        ticket_attachments = ticket.attachments.all()
        
        if 'body' in request.POST:
            # if the 'body' field is present in the POST data, create a new message
            message = Message.objects.create(
                user=request.user,
                ticket=ticket,
                body=request.POST.get('body')
            )
            ticket.participants.add(request.user)
            
        else:
            # if the 'body' field is not present, should be creating a new attachment 
            for file in request.FILES.getlist('files'):
                Attachment.objects.create(
                    file=file,
                    ticket=ticket
                )
            
        return redirect('ticket', pk=ticket.id)


@method_decorator(login_required, name='dispatch')
class UpdateTicketView(View):
    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, id=pk)
        if request.user != ticket.host:
            return HttpResponse('You are not allowed')
        assignee_ids = ticket.assignee.values_list('id', flat=True)
        form = TicketForm(instance=ticket, initial={'assignees': assignee_ids})
        # Get all users for the dropdown list
        users = CustomUser.objects.all()
        
        context = {'form': form, 'ticket': ticket, 'assignee_ids': assignee_ids, 'users': users}
        return render(request, 'tickets/ticket_form.html', context)

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, id=pk)
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.host = request.user
            
            # Get the current project based on the ticket's project ID
            project = get_object_or_404(Project, pk=ticket.project.id)
            ticket.project = project
            
            # Get the list of selected users and assign them to the ticket
            assignee_ids = request.POST.getlist('assignees')
            assignee_ids = [int(id) for id in assignee_ids]  # Convert to list of integers
            assignees = CustomUser.objects.filter(id__in=assignee_ids)
                
            ticket.save()
            ticket.assignee.set(assignees)  
            
            # create ticket history
            history = TicketHistory(
                ticket=ticket,
                updated_by=request.user,
                name=ticket.name,
                status=ticket.status,
                priority=ticket.priority,
                type=ticket.type,
                description=ticket.description,
            )
            history.save()

            
            
            return redirect('ticket', pk=ticket.id)
        context = {'form': form, 'ticket': ticket, 'assignee_ids': assignee_ids}
        return render(request, 'tickets/ticket_form.html', context)

@method_decorator(login_required, name='dispatch')
class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'tickets/ticket-delete.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        ticket = self.get_object()
        if request.user != ticket.host:
            return HttpResponse('You are not allowed')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class DeleteMessageView(View):
    template_name = 'tickets/delete.html'

    def get(self, request, pk):
        message = get_object_or_404(Message, id=pk, user=request.user)
        return render(request, self.template_name, {'obj': message})
    
    def post(self, request, pk):
        message = get_object_or_404(Message, id=pk, user=request.user)
        message.delete()
        return redirect('home')
    
def categoriesPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    categories = Category.objects.filter(name__icontains=q)
    return render(request, 'projects/categories.html', {'categories': categories})

def activityPage(request):
    ticket_messages = Message.objects.all()
    return render(request, 'projects/activity.html', {'ticket_messages': ticket_messages})