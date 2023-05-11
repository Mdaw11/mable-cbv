from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
from .models import Project
from django.core.paginator import Paginator
from .forms import ProjectForm
from tickets.forms import TicketForm
from django.db.models import Q
from tickets.models import Ticket
from users.models import CustomUser
from django.utils.html import strip_tags

# Create your views here.
def landingpage(request):
    
    return render(request, 'landingpage.html')


class ProjectHomeView(View):
    def get(self, request):
        user = request.user
        projects = Project.objects.filter(
            Q(user=request.user) |
            Q(assigned_users=user) | 
            Q(project__assignee=user)
        ).distinct()
        search_query = request.GET.get('search')
        form = ProjectForm()
        
        # Filter projects based on a search query
        if search_query:    
            projects = Project.objects.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        paginator = Paginator(projects, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'projects': projects, 
                   'page_obj': page_obj, 
                   'search_query': search_query,
                   'form': form,
                   }
        return render(request, 'projects/project_home.html', context)

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            data = {'success': True}
        else:
            data = {'success': False, 'errors': form.errors}
        
        return JsonResponse(data)
        
        
class ProjectView(View):
    def get(self, request, pk):
        project_id = Project.objects.get(id=pk)
        form = TicketForm(initial={'project': project_id})
        search_query = request.GET.get('search')
        tickets = Ticket.objects.filter(project=project_id)
        # Get the assigned users for the project and tickets
        assigned_users = CustomUser.objects.filter(assignee__in=tickets).distinct()
        
        # Search functionality
        if search_query:
            tickets = tickets.filter(
                Q(assignee__username__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(status__iexact=search_query) |
                Q(priority__icontains=search_query) |
                Q(type__icontains=search_query)
            )
            assigned_users = assigned_users.filter(
                Q(username__icontains=search_query)
            )
        # Get all users for the dropdown list
        users = CustomUser.objects.all()
            
        # Paginate the ticket table and assigned user tables
        paginator = Paginator(tickets, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        user_paginator = Paginator(assigned_users, 5)
        user_page_number = request.GET.get('user_page')
        user_page_obj = user_paginator.get_page(user_page_number)
        
        # Get the users assigned to each ticket
        ticket_assignees = []
        for ticket in tickets:
            assignees = ticket.assignee.all().distinct()
            ticket_assignees.append(assignees)
            

        context = {
            'project_id': project_id, 
            'tickets': tickets,
            'form': form,
            'page_obj': page_obj,
            'assigned_users': assigned_users,
            'user_page_obj': user_page_obj,
            'search_query': search_query,
            'users': users,
        }

        return render(request, 'projects/project.html', context)

    def post(self, request, pk):
    # Handle POST requests
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.host = request.user
            
            # Get the current project based on the passed ID
            project = get_object_or_404(Project, pk=pk)
            ticket.project = project
            
            # Get the list of selected users and assign them to the ticket
            assignee_ids = request.POST.getlist('assignees')
            assignee_ids = [int(id) for id in assignee_ids]  # Convert to list of integers
            assignees = CustomUser.objects.filter(id__in=assignee_ids)           
            
            # Set the description field to the value from the POST request
            # Process the description field separately to properly handle HTML content
            ticket.description = strip_tags(request.POST.get('description'))
            
            ticket.save()
            ticket.assignee.set(assignees)  # Assign after saving the ticket
                
            data = {
                'success': True,
            }
        else:
            data = {
                'success': False,
                'errors': form.errors,
            }
        return JsonResponse(data)
            

@method_decorator(login_required, name='dispatch')
class CreateProjectView(View):
    def get(self, request):
        form = ProjectForm()
        context = {'form': form}
        return render(request, 'projects/project_home.html', context)

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project-home')
        else:
            context = {'form': form}
            return render(request, 'projects/project_home.html', context)

@method_decorator(login_required, name='dispatch')
class UpdateProjectView(View):
    def get(self, request, pk):
        project = Project.objects.get(id=pk)
        form = ProjectForm(instance=project)
        context = {'form': form, 'project': project}
        return render(request, 'projects/project_form.html', context)

    def post(self, request, pk):
        project = Project.objects.get(id=pk)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project', pk=project.id)
        else:
            context = {'form': form, 'project': project}
            return render(request, 'projects/project_form.html', context)

@method_decorator(login_required, name='dispatch')
class DeleteProjectView(View):
    def get(self, request, pk):
        project = Project.objects.get(id=pk)
        return render(request, 'projects/project-delete.html', {'obj': project})

    def post(self, request, pk):
        project = Project.objects.get(id=pk)
        project.delete()
        return redirect('project-home')