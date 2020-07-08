from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('projects/', views.projects, name="projects"),
    path('projects/<int:project_id>/', views.project, name="project"),
    path('projects/<int:project_id>/sprints/', views.sprints, name="sprints"),
    path('projects/<int:project_id>/sprints/<int:sprint_id>/', views.sprint, name="sprint"),
    path('projects/<int:project_id>/pages/', views.pages, name="pages"),
    path('projects/<int:project_id>/pages/<int:page_id>/', views.page, name="page"),
]