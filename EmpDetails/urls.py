from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('employee', views.EmployeeViewSet, basename="employee")
router.register('leave', views.EmployeeLeaves, basename="leave")

urlpatterns = [
    path('register/', views.RegisterEmployeeView.as_view()),
    path('login/', views.LoginView.as_view()),
    # path('employee/', views.EmployeeAPIView.as_view()),
    path('', include(router.urls))
]