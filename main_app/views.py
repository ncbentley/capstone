from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Project, Sprint, Task, Page, Wireframe
from .forms import RegistrationForm
import json
# Create your views here.

def home(request):
    context = {'register_form': RegistrationForm(), 'login_form': AuthenticationForm()}
    return render(request, 'home.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            return JsonResponse({'success': 'true'})
        else:
            return JsonResponse({'error': 'Username or password is incorrect'})
    else: #Unauthorized
        pass


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first = request.POST.get('first_name')
            last = request.POST.get('last_name')
            email = request.POST.get('email')
            user_type = request.POST.get('user_type')
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = form.save()
            user.profile.full_name = f"{first} {last}"
            user.profile.email = email
            user.profile.user_type = user_type
            user.save()
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return JsonResponse({'success': 'true'})
        return JsonResponse({'error': form.errors})
    else: #Unauthorized
        pass


def projects(request):
    if request.method == 'GET': # Projects Index
        projects = Project.objects.filter(Q(client=request.user.profile) | Q(dev=request.user.profile))
        context = {projects: projects}
        return render(request, 'projects/index.html', context)
    elif request.method == 'POST': # TODO: Projects Create
        pass
    else: # TODO: Unauthorized
        pass

def project(request, project_id):
    if request.method == 'GET': # Project Show
        try:
            project = Project.objects.get(id=project_id)
            context = {project: project}
            return render(request, 'projects/show.html', context)
        except:
            return render(request, '404.html')
    elif request.method == 'PUT': # TODO: Project Update
        pass
    elif request.method == 'DELETE': # TODO: Project Delete
        pass
    else: # TODO: Unauthorized
        pass

def sprints(request, project_id):
    if request.method == 'GET': # Projects Index
        try:
            project = Project.objects.get(id=project_id)
            sprints = project.sprint_set.all()
            context = {project: project, sprints: sprints}
        except:
            return render(request, '404.html')
        return render(request, 'projects/sprints/index.html', context)
    elif request.method == 'POST': # TODO: Projects Create
        pass
    else: # TODO: Unauthorized
        pass

def sprint(request, project_id, sprint_id):
    if request.method == 'GET': # Project Show
        try:
            sprint = Sprint.objects.get(id=sprint_id)
            project = Project.objects.get(id=project_id)
            context = {project: project, sprint: sprint}
            return render(request, 'projects/sprints/show.html', context)
        except:
            return render(request, '404.html')
    elif request.method == 'PUT': # TODO: Project Update
        pass
    elif request.method == 'DELETE': # TODO: Project Delete
        pass
    else: # TODO: Unauthorized
        pass

def pages(request, project_id):
    if request.method == 'GET': # Projects Index
        try:
            project = Project.objects.get(id=project_id)
            pages = project.page_set.all()
            context = {project: project, pages: pages}
            return render(request, 'projects/pages/index.html', context)
        except:
            return render(request, '404.html')
    elif request.method == 'POST': # TODO: Projects Create
        pass
    else: # TODO: Unauthorized
        pass

def page(request, project_id, page_id):
    if request.method == 'GET': # Project Show
        try:
            page = Page.objects.get(id=page_id)
            project = Project.objects.get(id=project_id)
            context = {project: project, page: page}
            return render(request, 'projects/pages/show.html', context)
        except:
            return render(request, '404.html')
    elif request.method == 'PUT': # TODO: Project Update
        pass
    elif request.method == 'DELETE': # TODO: Project Delete
        pass
    else: # TODO: Unauthorized
        pass