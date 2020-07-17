from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Project, Sprint, Task, Page, Wireframe, Profile
from .forms import RegistrationForm, ProjectForm, PageForm, TaskForm, WireframeForm, ProfileForm, EditProjectForm
import json


def home(request):
    if request.user.is_authenticated:
        return redirect(projects)
    context = {'register_form': RegistrationForm(prefix="register"), 'login_form': AuthenticationForm(prefix="login")}
    try:
        context['profile_form'] = ProfileForm(instance=request.user.profile, prefix="profile")
    except:
        pass
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
            if 'project' in request.POST:
                project = Project.objects.get(id=request.POST.get('project'))
                project.client = user.profile
                project.save()
            return redirect('/')
        context = {'login_form': form, 'register_form': RegistrationForm(prefix="register"), 'login_error': 'true'}
        try:
            context['profile_form'] = ProfileForm(instance=request.user.profile, prefix="profile")
        except:
            pass
        if 'project' in request.POST:
            context['project_id'] = request.POST.get('project')
            return render(request, 'attach.html', context)
        return render(request, 'home.html', context)
    else:
        return render(request, '404.html')

def signup(request):
    email_error = False
    if request.method == 'POST': #Authenticate registration
        form = RegistrationForm(request.POST, prefix="register")
        if form.is_valid():
            first = request.POST.get('register-first_name')
            last = request.POST.get('register-last_name')
            email = request.POST.get('register-email')
            user_type = request.POST.get('register-user_type')
            username = request.POST.get('register-username')
            password = request.POST.get('register-password1')
            try:
                profile = Profile.objects.get(email=email)
                if 'profile' in request.POST:
                    return render(request, 'attach.html', {'login_form': AuthenticationForm(prefix="login"), 'register_form': form, 'register_error': 'true', 'project_id': request.POST.get('project'), 'email_error': 'true'})
                else:
                    return render(request, 'home.html', {'login_form': AuthenticationForm(prefix="login"), 'register_form': form, 'register_error': 'true'})
            except:
                pass
            user = form.save()
            user.profile.full_name = f"{first} {last}"
            user.profile.email = email
            user.profile.user_type = user_type
            user.save()
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            if 'project' in request.POST:
                project = Project.objects.get(id=request.POST.get('project'))
                project.client = user.profile
                project.save()
            return redirect('/')
        context = {'login_form': AuthenticationForm(prefix="login"), 'register_form': form, 'register_error': 'true'}
        try:
            context['profile_form'] = ProfileForm(instance=request.user.profile, prefix="profile")
        except:
            pass
        if 'project' in request.POST:
            context = {'login_form': AuthenticationForm(prefix="login"), 'register_form': form, 'register_error': 'true', 'project_id': request.POST.get('project')}
            return render(request, 'attach.html', context)
        return render(request, 'home.html', context)
    else: 
        return render(request, '404.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect(home)

def attach(request, project_id):
    context = {'register_form': RegistrationForm(prefix="register"), 'login_form': AuthenticationForm(prefix="login"), 'project_id': project_id}
    return render(request, 'attach.html', context)

@login_required
def image(request, wireframe_id):
    try: # Render full size image page
        wireframe = Wireframe.objects.get(id=wireframe_id)
        return render(request, 'image.html', {'wireframe': wireframe})
    except: # If broken link
        return render(request, '404.html')

@login_required
def profile(request, profile_id):
    if request.method == 'POST' and request.POST.get('_method') == 'PUT': # Update Profile
        profile = Profile.objects.get(id=profile_id)
        if request.user.profile != profile:
            return redirect(home)
        ProfileForm(request.POST, prefix="profile", instance=profile).save()
    return redirect(home)

@login_required
def projects(request):
    error = False
    if request.method == 'POST' and request.user.profile.user_type == 'dev': # Projects Create
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.dev = request.user.profile
            # TODO: Attach to client if email. If not return a unique link to give to the client
            try: # This checks if the email given is valid
                client = Profile.objects.get(email=request.POST.get("client_email"))
                project.client = client
                project.save()
                return redirect(f'/projects/{project.id}/')
            except:
                project.save()
                return redirect(f'/projects/{project.id}/')
        error = True
    else:
        form = ProjectForm()
    projects = Project.objects.filter(Q(client=request.user.profile) | Q(dev=request.user.profile))
    context = {'register_form': RegistrationForm(prefix="register"), 'login_form': AuthenticationForm(prefix="login"), 'profile_form': ProfileForm(prefix="profile"), 'projects': projects, 'form': form}
    if error:
        context['create_error'] = 'true'
    context['profile_form'] = ProfileForm(instance=request.user.profile, prefix="profile")
    return render(request, 'projects/index.html', context)

@login_required
def project(request, project_id):
    if request.method == 'GET': # Project Show
        try:
            project = Project.objects.get(id=project_id)
            context = {'register_form': RegistrationForm(prefix="register"), 'login_form': AuthenticationForm(prefix="login"), 'project': project, 'page_form': PageForm(), 'project_form': EditProjectForm(instance=project)}
            try:
                context['profile_form'] = ProfileForm(instance=request.user.profile, prefix="profile")
            except:
                pass
            return render(request, 'projects/show.html', context)
        except Exception as e:
            print(e)
            return render(request, '404.html')
    elif request.method == 'POST' and request.POST.get('_method') == 'PUT' and request.user.profile.user_type == 'client': # Project Update
        project = Project.objects.get(id=project_id)
        form = EditProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
        return redirect(f'/projects/{project_id}/')
    elif request.method == 'POST' and request.POST.get('_method') == 'DELETE' and request.user.profile.user_type == 'client': # Project Delete
        project = Project.objects.get(id=project_id)
        project.delete()
        return redirect(projects)
    else:
        return render(request, '404.html')

@login_required
def sprints(request, project_id):
    if request.method == 'POST' and request.user.profile.user_type == 'client': # Sprints Create
        try:
            sprint = Sprint(project=Project.objects.get(id=project_id))
            sprint.save()
            return redirect(f'/projects/{project_id}/sprints/{sprint.id}')
        except:
            return redirect(project, project_id)
    else:
        return render(request, '404.html')

@login_required
def sprint(request, project_id, sprint_id):
    if request.method == 'GET': # Sprint Show
        try:
            sprint = Sprint.objects.get(id=sprint_id)
            project = sprint.project
            for x, s in enumerate(project.sprint_set.all()):
                if s.id == sprint.id:
                    break
            context = {'register_form': RegistrationForm(prefix="register"), 'login_form': AuthenticationForm(prefix="login"), 'sprint': sprint, 'task_form': TaskForm(), 'number': x + 1}
            try:
                context['profile_form'] = ProfileForm(instance=request.user.profile, prefix="profile")
            except:
                pass
            return render(request, 'projects/sprints/show.html', context)
        except Exception as e:
            print(e)
            return render(request, '404.html')
    elif request.method == 'POST' and request.POST.get('_method') == 'DELETE' and request.user.profile.user_type == 'client': # TODO: Sprint Delete
        sprint = Sprint.objects.get(id=sprint_id)
        sprint.delete()
        return redirect(f'/projects/{project_id}/')
    else:
        return render(request, '404.html')

@login_required
def tasks(request, project_id, sprint_id):
    if request.method == 'POST' and request.user.profile.user_type == 'client': # Task Create
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                task = form.save(commit=False)
                task.sprint = Sprint.objects.get(id=sprint_id)
                task.save()
                return redirect(sprint, project_id, sprint_id)
            except:
                pass
        return redirect(project, project_id)     
    else:
        return render(request, '404.html')

@login_required
def task(request, project_id, sprint_id, task_id):
    if request.method == 'POST' and request.POST.get("_method") == 'PUT' and request.user.profile.user_type == 'client': # Task Update
        try:
            task = Task.objects.get(id=task_id)
            task.description = request.POST.get('description')
            task.save()
        except:
            pass
        return redirect(sprint, project_id, sprint_id)
    elif request.method == 'POST' and request.POST.get('_method') == "DELETE" and request.user.profile.user_type == 'client': # Task Delete
        task = Task.objects.get(id=task_id)
        if task.sprint.project.client == request.user.profile:
            task.delete()
        return redirect(sprint, project_id, sprint_id)
    else:
        return render(request, '404.html')

@login_required
def pages(request, project_id):
    if request.method == 'POST' and request.user.profile.user_type == 'client': # Pages Create
        form = PageForm(request.POST)
        if form.is_valid():
            try:
                page = form.save(commit=False)
                page.project = Project.objects.get(id=project_id)
                page.save()
                return redirect(project, project_id)
            except: pass
        return redirect(project, project_id)
    else:
        return render(request, '404.html')

@login_required
def page(request, project_id, page_id):
    if request.method == 'GET': # Page Show
        try:
            page = Page.objects.get(id=page_id)
            wireframes = page.wireframe_set.all()
            context = {'register_form': RegistrationForm(prefix="register"), 'login_form': AuthenticationForm(prefix="login"), 'page': page, 'wireframe_form': WireframeForm(), 'edit_forms': [], 'wireframes': wireframes, 'page_form': PageForm(instance=page)}
            try:
                context['profile_form'] = ProfileForm(instance=request.user.profile, prefix="profile")
            except:
                pass
            # Send form for each wireframe edit actions
            for wireframe in wireframes:
                context['edit_forms'].append(WireframeForm(instance=wireframe))
            return render(request, 'projects/pages/show.html', context)
        except Exception as e:
            return render(request, '404.html')
    elif request.method == 'POST' and request.POST.get('_method') == 'PUT' and request.user.profile.user_type == 'client': # Page Edit
        try:
            page = Page.objects.get(id=page_id)
            form = PageForm(request.POST, instance=page)
            if form.is_valid():
                form.save()
        except:
            pass
        return redirect(f'/projects/{project_id}/pages/{page_id}')
    elif request.method == 'POST' and request.POST.get('_method') == 'DELETE' and request.user.profile.user_type == 'client': # Page Delete
        try:
            page = Page.objects.get(id=page_id)
            page.delete()
        except:
            pass
        return redirect(project, project_id)
    else:
        return render(request, '404.html')

@login_required
def wireframes(request, project_id, page_id):
    if request.method == 'POST' and request.user.profile.user_type == 'client': # Wireframe Create
        form = WireframeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                wireframe = form.save(commit=False)
                wireframe.page = Page.objects.get(id=page_id)
                wireframe.save()
                return redirect(page, project_id, page_id)
            except:
                pass
        return redirect(project, project_id)
    else:
        return render(request, '404.html')

@login_required
def wireframe(request, project_id, page_id, wireframe_id):
    if request.method == 'POST' and request.POST.get('_method') == 'PUT' and request.user.profile.user_type == 'client': # Wireframe Update
        form = WireframeForm(request.POST, request.FILES, instance=Wireframe.objects.get(id=wireframe_id)).save()
        return redirect(page, project_id, page_id)
    elif request.method == 'POST' and request.POST.get('_method') == 'DELETE' and request.user.profile.user_type == 'client': #  Wireframe Delete
        wireframe = Wireframe.objects.get(id=wireframe_id)
        wireframe.delete()
        return redirect(page, project_id, page_id)
    else:
        return render(request, '404.html')

@login_required
def toggle_complete(request, task_id):
    if request.user.profile.user_type == 'dev':
        try:
            task = Task.objects.get(id=task_id)   
            if task.sprint.project.dev == request.user.profile:
                task.completed = not task.completed
                task.save()
            return JsonResponse({})
        except Exception as e:
            print(e)
    return JsonResponse({})
