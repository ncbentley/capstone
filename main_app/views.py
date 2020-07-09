from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Project, Sprint, Task, Page, Wireframe, Profile
from .forms import RegistrationForm, ProjectForm
import json

# TODO: LoginRequired

def home(request):
    context = {'register_form': RegistrationForm(prefix="register"), 'login_form': AuthenticationForm(prefix="login")}
    return render(request, 'home.html', context)

def login(request):
    if request.method == 'POST': # Authenticate Login\
        print(request.POST)
        form = AuthenticationForm(request.POST, prefix="login")
        username = request.POST.get('login-username')
        password = request.POST.get('login-password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            return redirect('/')
        
        return render(request, 'home.html', {'login_form': form, 'register_form': RegistrationForm(prefix="register"), 'login_error': 'true'})
    else: # TODO: Unauthorized
        pass


def signup(request):
    if request.method == 'POST': #Authenticate registration
        form = RegistrationForm(request.POST, prefix="register")
        if form.is_valid():
            first = request.POST.get('register-first_name')
            last = request.POST.get('register-last_name')
            email = request.POST.get('register-email')
            user_type = request.POST.get('register-user_type')
            username = request.POST.get('register-username')
            password = request.POST.get('register-password1')
            user = form.save()
            user.profile.full_name = f"{first} {last}"
            user.profile.email = email
            user.profile.user_type = user_type
            user.save()
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('/')
        return render(request, 'home.html', {'login_form': AuthenticationForm(prefix="login"), 'register_form': form, 'register_error': 'true'})
    else: # TODO: Unauthorized
        pass


def projects(request):
    if request.method == 'GET': # Projects Index
        projects = Project.objects.filter(Q(client=request.user.profile) | Q(dev=request.user.profile))
        context = {'projects': projects, 'form': ProjectForm()}
        return render(request, 'projects/index.html', context)
    elif request.method == 'POST': # TODO: Projects Create
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.dev = request.user.profile
            try:
                project.client = Profile.objects.get(email=request.POST.get("client_email"))
                project.save()
                return redirect(f'/projects/{project.id}')
            except Exception as e:
                print(e)
                pass
        projects = Project.objects.filter(Q(client=request.user.profile) | Q(dev=request.user.profile))
        return render(request, 'projects/index.html', {'projects': projects, 'form': form, 'create_error': 'true'})
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