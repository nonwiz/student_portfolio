from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import *
from random import randint
from django import forms
from .forms import StudentForm
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Logout user
def logout_user(req):
    logout(req)
    return redirect('spapp:login')



# Student Pages
class LoginPage(generic.TemplateView):
    template_name = "pages/auth/student_login.html"
    dashboard_template = "pages/student/dashboard.html"

    def post(self, req):
        #print("Post request at Login")
        #print("Request: ", req.POST)
        """ getting inputs from the form based on the name specified on the inputs fields 
            POST is used to pass information from the client side to the server
        """
        username, password = req.POST['username'], req.POST['password']

        """ checking if the username and password are correct (based on registered accounts) 
        You can write your own authentication method, but in our case thanks to django we don't 
        need to do that, we can rely on the autheication function they already have (by importing the function, check line 3)

        the authentication checks if the user exists, and also if the password matches the password for that user. if its all correct
        then an object will be stored in user.
    """
        user = authenticate(req, username=username, password=password)
        if user is not None:
            """ (on line 27 we assigned an object to the variable user, and if its not empty we login and redirect them tot he dashboard) """
            # Below here is to tell the user about their username
            login(req, user)
            return redirect('spapp:dashboard')
        else:
            #print("User is not found in database")
            """ if login failed we redirect them back to the login page """
            return render(req, self.template_name)


class DashboardPage(LoginRequiredMixin, generic.TemplateView):
    login_url = 'spapp:login'
    template_name = "pages/student/dashboard.html"



class RegisterPage(generic.TemplateView):
    template_name = "pages/auth/student_register.html"

    def post(self, req):
        print("After you click sign up, here is the info available", req.POST)
        """getting input from the form fields using the POST method in the request and store them as a dictionary (key and value)"""
        data = req.POST
        full_name = data['full_name']  # get full name from the submited input
        id_number = data["id_number"]
        
        if len(id_number) != 9:
            messages.add_message(req, messages.WARNING, "Invalid ID Number")
            return render(req,  self.template_name)
        try:
            id_number = int(id_number)
        except ValueError:
            messages.add_message(req, messages.WARNING, "Invalid ID Number")
            print("Not numbers")
            return render(req,  self.template_name)
        arr_full_name = full_name.split(" ")
        # retreive first and last name from the full name
        first_name, last_name = arr_full_name[0], arr_full_name[-1]
        username = str(id_number)

        """ check if the password are the same, if they are not, then return 'wrong password' else continue saving the user """
        if data['password'] != data['password1']:
            messages.add_message(req, messages.WARNING, "Confirm password is not the same as password")
            return render(req,  self.template_name)
        """ register the user account """
        user = User.objects.create_user(
            username, data['email'], data['password'])
        user.first_name, user.last_name = first_name, last_name
        user.save()
        """ using the registered user add thier information in the student table """
        student = Student(user=user, id_number=username)
        student.save()
        """redirect the user to the dashboard after they signup (log them in) """
        user = authenticate(req, username=username, password=data['password'])
        if user is not None:
            messages.add_message(req, messages.SUCCESS, "You successfully created your account.")
            login(req, user)
            return redirect('spapp:dashboard')
        messages.add_message(req, messages.INFO, "You can try to login.")
        return render(req,  self.template_name)
 
class ProfilePage(LoginRequiredMixin, generic.TemplateView):
    login_url = 'spapp:login'
    template_name = "pages/student/profile.html"


 
class SettingTestPage(LoginRequiredMixin, generic.UpdateView):
    login_url = 'spapp:login'
    template_name = "components/student/update_account_detail.html"
    form_class = StudentForm

    def get_object(self):
        return get_object_or_404(Student, id=self.kwargs.get('pk'))

   

class SettingsPage(LoginRequiredMixin, generic.TemplateView):
    login_url = 'spapp:login'
    template_name = "pages/student/settings.html"
    form_update_student = StudentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # If Found student account is not found within the Request, return True.
            context['student'] = Student.objects.get(user=self.request.user)
            context['update_student'] = self.form_update_student()
            context['account_status'] = not bool(len(AccountRemovalRequest.objects.filter(student=self.request.user.student)))
            return context
        except:
            messages.add_message(self.request, messsages.WARNING, "You are not a student")
            return context
    def post(self, req):
        try:
            data = req.POST.dict()
            update_student = self.form_update_student(data)
            if update_student.is_valid():
                student = Student.objects.get_object_or_404(user=req.user)
                form = self.form_update_student(update_student.cleaned_data, instance=student)
                form.save()
            else:
                messages.add_message(req, messages.INFO, update_student.errors.as_text)
        except:
            messages.add_message(req, messages.WARNING, "Unable to update the current student data.") 
        return redirect("spapp:settings")


# Student request to remove their account
def remove_account_request(req):
    # For the future: we can create a switch to allow student to request and remove the request
    # removal_request = req.user.student.account_removal_request
    removal_request = AccountRemovalRequest.objects.filter(
        student=req.user.student).first()
    print(removal_request)
    if removal_request is not None:
        print("You already requested!")
        return redirect("spapp:profile")
    removal_request = AccountRemovalRequest.objects.create(
        student=req.user.student)
    messages.add_message(req, messages.WARNING, "Request to remove account has been sented")
    print("Requesting account Removal successfully")
    return redirect('spapp:settings')

