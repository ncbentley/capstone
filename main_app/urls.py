from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('attach/<int:project_id>/', views.attach, name="attach"),
    path('image/<int:wireframe_id>/', views.image, name="image"),
    path('profile/<int:profile_id>/', views.profile, name="profile"),
    path('projects/', views.projects, name="projects"),
    path('projects/<int:project_id>/', views.project, name="project"),
    path('projects/<int:project_id>/sprints/', views.sprints, name="sprints"),
    path('projects/<int:project_id>/sprints/<int:sprint_id>/', views.sprint, name="sprint"),
    path('projects/<int:project_id>/sprints/<int:sprint_id>/tasks', views.tasks, name='tasks'),
    path('projects/<int:project_id>/sprints/<int:sprint_id>/tasks/<int:task_id>', views.task, name='task'),
    path('projects/<int:project_id>/pages/', views.pages, name="pages"),
    path('projects/<int:project_id>/pages/<int:page_id>/', views.page, name="page"),
    path('projects/<int:project_id>/pages/<int:page_id>/wireframes/', views.wireframes, name="wireframes"),
    path('projects/<int:project_id>/pages/<int:page_id>/wireframe/<int:wireframe_id>/', views.wireframe, name="wireframe"),
    path('togglecomplete/<int:task_id>/', views.toggle_complete, name="togglecomplete")
]