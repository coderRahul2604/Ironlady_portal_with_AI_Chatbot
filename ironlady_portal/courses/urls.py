from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course-list'),
    path('course/add/', views.CourseCreateView.as_view(), name='course-add'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('course/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course-edit'),
    path('course/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),
]
