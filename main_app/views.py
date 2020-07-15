from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Project, Sprint, Task, Page, Wireframe, Profile
from .forms import RegistrationForm, ProjectForm, PageForm, TaskForm, WireframeForm, ProfileForm
import json

# TODO: LoginRequired

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
            return redirect('/')
        context = {'login_form': form, 'register_form': RegistrationForm(prefix="register"), 'login_error': 'true'}
        try:
            context['profile_form'] = ProfileForm(instance=request.user.profile, prefix="profile")
        except:
            pass
        return render(request, 'home.html', context)
    else:
        return render(request, '404.html')


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
        context = {'login_form': AuthenticationForm(prefix="login"), 'register_form': form, 'register_error': 'true'}
        try:
            context['profile_form'] = ProfileForm(instance=request.user.profile, prefix="profile")
        except:
            pass
        return render(request, 'home.html', context)
    else: 
        return render(request, '404.html')

def logout(request):
    auth_logout(request)
    return redirect(home)

def image(request, wireframe_id):
    try:
        wireframe = Wireframe.objects.get(id=wireframe_id)
        return render(request, 'image.html', {'wireframe': wireframe})
    except:
        return render(request, '404.html')

def profile(request, profile_id):
    if request.method == 'POST' and request.POST.get('_method') == 'PUT': # Update Profile
        profile = Profile.objects.get(id=profile_id)
        if request.user.profile != profile:
            return redirect(home)
        ProfileForm(request.POST, prefix="profile", instance=profile).save()
    print(request.POST)
    return redirect(request.POST.get('origin'))


def projects(request):
    error = False
    if request.method == 'POST': # Projects Create
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.dev = request.user.profile
            try:
                project.client = Profile.objects.get(email=request.POST.get("client_email"))
                project.save()
                return redirect(project, project.id)
            except:
                pass
        error = True
    else:
        form = ProjectForm()
    projects = Project.objects.filter(Q(client=request.user.profile) | Q(dev=request.user.profile))
    context = {'register_form': RegistrationForm(prefix="register"), 'login_form': AuthenticationForm(prefix="login"), 'profile_form': ProfileForm(prefix="profile"), 'projects': projects, 'form': form}
    if error:
        context['create_error'] = 'true'
    try:
        context['profile_form'] = ProfileForm(instance=request.user.profile, prefix="profile")
    except:
        pass
    return render(request, 'projects/index.html', context)


def project(request, project_id):
    if request.method == 'GET': # Project Show
        try:
            project = Project.objects.get(id=project_id)
            context = {'register_form': RegistrationForm(prefix="register"), 'login_form': AuthenticationForm(prefix="login"), 'project': project, 'page_form': PageForm()}
            try:
                context['profile_form'] = ProfileForm(instance=request.user.profile, prefix="profile")
            except:
                pass
            return render(request, 'projects/show.html', context)
        except Exception as e:
            print(e)
            return render(request, '404.html')
    elif request.method == 'PUT': # TODO: Project Update
        pass
    elif request.method == 'DELETE': # TODO: Project Delete
        pass
    else:
        return render(request, '404.html')

def sprints(request, project_id):
    if request.method == 'POST': # Sprints Create
        try:
            sprint = Sprint(project=Project.objects.get(id=project_id))
            sprint.save()
            return redirect(sprint, project_id, sprint.id)
        except:
            return redirect(projects)
    else:
        return render(request, '404.html')

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
    elif request.method == 'POST' and request.POST.get('_method') == 'DELETE': # TODO: Sprint Delete
        pass
    else:
        return render(request, '404.html')

def tasks(request, project_id, sprint_id):
    if request.method == 'POST': # Task Create
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

def task(request, project_id, sprint_id, task_id):
    if request.method == 'POST' and request.POST.get("_method") == 'PUT': # Task Update
        try:
            task = Task.objects.get(id=task_id)
            task.description = request.POST.get('description')
            task.save()
        except:
            pass
        return redirect(sprint, project_id, sprint_id)
    elif request.method == 'POST' and request.POST.get('_method') == "DELETE": # Task Delete
        task = Task.objects.get(id=task_id)
        if task.sprint.project.client == request.user.profile:
            task.delete()
        return redirect(sprint, project_id, sprint_id)
    else:
        return render(request, '404.html')

def pages(request, project_id):
    if request.method == 'POST': # Pages Create
        form = PageForm(request.POST)
        if form.is_valid():
            try:
                page = form.save(commit=False)
                page.project = Project.objects.get(id=project_id)
                page.save()
                return redirect(page, project_id, page.id)
            except: pass
        return redirect(projects)
    else:
        return render(request, '404.html')

def page(request, project_id, page_id):
    if request.method == 'GET': # Page Show
        try:
            page = Page.objects.get(id=page_id)
            wireframes = page.wireframe_set.all()
            context = {'register_form': RegistrationForm(prefix="register"), 'login_form': AuthenticationForm(prefix="login"), 'page': page, 'wireframe_form': WireframeForm(), 'edit_forms': [], 'wireframes': wireframes}
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
    elif request.method == 'POST' and request.POST.get('_method') == 'PUT': # TODO: Page Update
        pass
    elif request.method == 'POST' and request.POST.get('_method') == 'DELETE': # TODO: Page Delete
        pass
    else:
        return render(request, '404.html')

def wireframes(request, project_id, page_id):
    if request.method == 'POST': # Wireframe Create
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

def wireframe(request, project_id, page_id, wireframe_id):
    if request.method == 'POST' and request.POST.get('_method') == 'PUT': # Wireframe Update
        form = WireframeForm(request.POST, request.FILES, instance=Wireframe.objects.get(id=wireframe_id)).save()
        return redirect(page, project_id, page_id)
    elif request.method == 'POST' and request.POST.get('_method') == 'DELETE': #  Wireframe Delete
        wireframe = Wireframe.objects.get(id=wireframe_id)
        wireframe.delete()
        return redirect(page, project_id, page_id)
    else:
        return render(request, '404.html')

def toggle_complete(request, task_id):
    try:
        task = Task.objects.get(id=task_id)   
        if task.sprint.project.dev == request.user.profile:
            task.completed = not task.completed
            task.save()
        return JsonResponse({})
    except Exception as e:
        print(e)
    return JsonResponse({})