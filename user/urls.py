from django.urls import path
from . import views

urlpatterns = [
    path('profile/client/', views.ClientProfileView.as_view(), name='client-profile'),
    path('profile/agent/', views.AgentProfileView.as_view(), name='agent-profile'),
    path('profile/owner/', views.OwnerProfileView.as_view(), name='owner-profile'), 
    path('profile/tenant', views.TenantProfileView.as_view(), name='tenant-profile'),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("get_csrf_token/", views.get_csrf_token, name="get_csrf_token"),

    path("profile/tenant/", views.TenantProfileView.as_view(), name="tenant-profile"),
    path("verify/", views.VerificationView.as_view(), name="verify"),
    path("appointment/", views.AppointmentView.as_view(), name="appointment"),

    path("check_authentication/", views.check_authentification, name="check_authentification"),

    path("verify/", views.VerificationView.as_view(), name="verify-user"),
]
