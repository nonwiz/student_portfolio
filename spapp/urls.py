from django.urls import path
from . import views

app_name = "spapp"


# Student URL Patterns
urlpatterns = [
    # Auth paths
    path("register", views.RegisterPage.as_view(), name="register"),
    path("login", views.LoginPage.as_view(), name="login"),
    path("logout", views.logout_user, name="logout"),

    path('', views.DashboardPage.as_view(), name='dashboard'),
    path("profile", views.ProfilePage.as_view(), name="profile"),
    path("settings", views.SettingsPage.as_view(), name="settings"),
    path("req_remove_account", views.remove_account_request,
         name="req_remove_account"),
    # url for creating validator
    path("create-academic-recognition", views.create_ar, name="create-ar"),
    path("update-academic-recognition/<pk>/",
         views.update_ar, name="update-ar"),
    path("create-validator", views.create_validator, name="create-validator"),
]

# Admin URL Patterns
urlpatterns += [
    path("manager", views.AdminDashboard.as_view(), name="manager_dashboard"),
    path("manager/settings", views.AdminSettings.as_view(), name="manager_settings"),
    path("manager/create/degree", views.create_degree, name="create_degree"),
    path("manager/create/major", views.create_major, name="create_major"),
    path("manager/create/emphasis", views.create_emphasis, name="create_emphasis"),
    path("manager/create/validator",
         views.create_validator, name="create_validator"),
    path("manager/delete/degree/<int:pk>", views.delete_degree, name="delete_degree")


]
