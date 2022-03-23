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
    # url for managing academic recognition
    path("update-ar/<pk>/", views.ARUpdateView.as_view(), name="update-ar"),
    # url for creating validator
    path("create-ar", views.create_ar, name="create-ar"),
    path("create-cs", views.create_cs, name="create-cs"),
    path("create-project", views.create_project, name="create-project"),
    path("create-research", views.create_research, name="create-research"),
    path("create-internship", views.create_internship, name="create-internship"),
    path("create-pj", views.create_pj, name="create-pj"),
    
    path("create-validator", views.create_validator, name="create-validator"),
]

# Admin URL Patterns
urlpatterns += [
    path("manager", views.AdminDashboard.as_view(), name="manager_dashboard"),
    path("manager/settings", views.AdminSettings.as_view(), name="manager_settings"),
    path("manager/create/degree", views.create_degree, name="create_degree"),
    path("manager/create/major", views.create_major, name="create_major"),
    path("manager/create/emphasis", views.create_emphasis, name="create_emphasis"),
    path("manager/create/job", views.create_job, name="create_job"),
    path("manager/create/validator",
         views.create_validator, name="create_validator"),
    path("manager/delete/degree/<int:pk>", views.delete_degree, name="delete_degree"),
    path("manager/delete/major/<int:pk>", views.delete_major, name="delete_major"),
    path("manager/delete/job/<int:pk>", views.delete_job, name="delete_job"),
    path("manager/delete/emphasis/<int:pk>", views.delete_emphasis, name="delete_emphasis"),
    path("manager/delete/validator/<int:pk>", views.delete_validator, name="delete_validator"),

    path("manager/edit/degree/<int:pk>", views.edit_degree, name="edit_degree"),
    path("manager/edit/job/<int:pk>", views.edit_job, name="edit_job"),
    path("manager/update/degree", views.update_degree, name="update_degree"),

    path("manager/edit/major/<int:pk>", views.edit_major, name="edit_major"),
    path("manager/update/major", views.update_major, name="update_major"),
    path("manager/update/job", views.update_job, name="update_job"),

    path("manager/edit/emphasis/<int:pk>", views.edit_emphasis, name="edit_emphasis"),
    path("manager/update/emphasis", views.update_emphasis, name="update_emphasis"),


    path("manager/edit/validator/<int:pk>", views.edit_validator, name="edit_validator"),
    path("manager/update/validator", views.update_validator, name="update_validator")



]
