from datetime import date
from random import randint

from django import forms
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from spapp.models import Student

from .forms import *
from .models import *


# Logout user
def logout_user(req):
    logout(req)
    return redirect('spapp:login')


# Student Pages
class LoginPage(generic.TemplateView):
    template_name = "pages/auth/login.html"
    dashboard_template = "pages/student/dashboard.html"

    def post(self, req):
        # print("Post request at Login")
        # print("Request: ", req.POST)
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
            if not user.is_staff:
                return redirect('spapp:dashboard')
            return redirect("spapp:manager_dashboard")
        else:
            # print("User is not found in database")
            """ if login failed we redirect them back to the login page """
            return render(req, self.template_name)


class DashboardPage(LoginRequiredMixin, generic.TemplateView):
    login_url = 'spapp:login'
    template_name = "pages/student/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            student = Student.objects.get(user=self.request.user)
            context = {
                'activities': Activity.objects.filter(student=student),
                'academic_recogs': AcademicRecognition.objects.filter(activity__student=student),
                'activity_form': ActivityForm,
                'ar_form': ARForm,
                'cs_form': CSForm,
                'project_form': ProjectForm,
                'research_form': ResearchForm,
                'internship_form': InternshipForm,
                'pj_form': PJForm,
                'v_form': ValidatorForm
            }
        except:
            print("Admin")
        return context


def create_ar(req):
    try:
        activity = Activity.objects.create(
            student=req.user.student, activity_name="Academic Recognition")
        semester = req.POST.get('semester')
        semester, gpa, year = req.POST['semester'], req.POST['gpa'], req.POST['year']
        AcademicRecognition.objects.create(
            activity=activity, semester=semester, gpa=gpa, year=year)
    except:
        print('Current logged in user is not a student!')
    return redirect('spapp:dashboard')

def create_cs(req):
    try:
        data = req.POST.dict()
        activity = Activity.objects.create(
            student=req.user.student, activity_name="Community Service", description=data["description"], from_date=date.fromisoformat(data['from_date']), to_date=date.fromisoformat(data['to_date']), validator=Validator.objects.get(pk=data["validator"])  )
        CommunityService.objects.create(
            activity=activity, location=data["location"]
        )
    except:
        print('Current logged in user is not a student!')
    return redirect('spapp:dashboard')

def create_project(req):
    try:
        data = req.POST.dict()
        activity = Activity.objects.create(
            student=req.user.student, activity_name="Project", description=data["description"], from_date=date.fromisoformat(data['from_date']), to_date=date.fromisoformat(data['to_date']), validator=Validator.objects.get(pk=data["validator"])  )
        Project.objects.create(
            activity=activity, location=data["location"], responsibility=data["responsibility"]
        )
    except:
        print('Current logged in user is not a student!')
    return redirect('spapp:dashboard')


def create_research(req):
    try:
        data = req.POST.dict()
        activity = Activity.objects.create(
            student=req.user.student, activity_name="Research", description=data["description"], from_date=date.fromisoformat(data['from_date']), to_date=date.fromisoformat(data['to_date']), validator=Validator.objects.get(pk=data["validator"])  )
        Research.objects.create(
            activity=activity, co_authors=data["co_authors"], link=data["link"], published_date=date.fromisoformat(data["published_date"])
        )
    except:
        print('Current logged in user is not a student!')
    return redirect('spapp:dashboard')


def create_internship(req):
    try:
        data = req.POST.dict()
        activity = Activity.objects.create(
            student=req.user.student, activity_name="Internship", description=data["description"], from_date=date.fromisoformat(data['from_date']), to_date=date.fromisoformat(data['to_date']), validator=Validator.objects.get(pk=data["validator"])  )
        Internship.objects.create(
            activity=activity
        )
    except:
        print('Current logged in user is not a student!')
    return redirect('spapp:dashboard')


# Previous job form
def create_pj(req):
    try:
        data = req.POST.dict()
        activity = Activity.objects.create(
            student=req.user.student, activity_name="Previous Job", description=data["description"], from_date=date.fromisoformat(data['from_date']), to_date=date.fromisoformat(data['to_date']), validator=Validator.objects.get(pk=data["validator"])  )
        PreviousJob.objects.create(
            activity=activity
        )
    except:
        print('Current logged in user is not a student!')
    return redirect('spapp:dashboard')



def update_ar(req, pk):
    form = ARForm(instance=AcademicRecognition.objects.get(
        id=pk), data=req.POST)
    if form.is_valid:
        form.save()
    return redirect('spapp:dashboard')


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
            messages.add_message(req, messages.WARNING,
                                 "Confirm password is not the same as password")
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
            messages.add_message(req, messages.SUCCESS,
                                 "You successfully created your account.")
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
            context['student'] = get_object_or_404(
                Student, user=self.request.user)
            context['update_student'] = self.form_update_student()
            context['account_status'] = not bool(
                len(AccountRemovalRequest.objects.filter(student=self.request.user.student)))
            return context
        except:
            messages.add_message(
                self.request, messages.WARNING, "You are not a student")
            return context

    def post(self, req):
        try:
            data = req.POST.dict()
            update_student = self.form_update_student(data)
            if update_student.is_valid():
                student = Student.objects.get_object_or_404(user=req.user)
                form = self.form_update_student(
                    update_student.cleaned_data, instance=student)
                form.save()
            else:
                messages.add_message(req, messages.INFO,
                                     update_student.errors.as_text)
        except:
            messages.add_message(req, messages.WARNING,
                                 "Unable to update the current student data.")
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
    messages.add_message(req, messages.WARNING,
                         "Request to remove account has been sented")
    print("Requesting account Removal successfully")
    return redirect('spapp:settings')


# Administrator Views

decorators = [staff_member_required(login_url='spapp:login')]


@method_decorator(decorators, name='dispatch')
class AdminDashboard(LoginRequiredMixin, generic.TemplateView):
    login_url = "spapp:login"
    template_name = "pages/manager/dashboard.html"


@method_decorator(decorators, name='dispatch')
class AdminSettings(LoginRequiredMixin, generic.TemplateView):
    login_url = "spapp:login"
    template_name = "pages/manager/settings.html"
    form_degree = DegreeForm
    form_major = MajorForm
    form_emphasis = EmphasisForm
    form_validator = ValidatorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context = {
                'degrees': Degree.objects.all(),
                'majors': Major.objects.all(),
                'emphasises': Emphasis.objects.all(),
                'validators': Validator.objects.all(),
                'form_degree': self.form_degree(),
                'form_major': self.form_major(),
                'form_emphasis': self.form_emphasis(),
                'form_validator': self.form_validator()
            }
            return context
        except:
            messages.add_message(
                self.request, messages.WARNING, "You are not a student")
            return context

    def post(self, req):
        try:
            data = req.POST.dict()
            print("SENT to POST", data)
        except:
            messages.add_message(req, messages.WARNING,
                                 "Unable to update the current student data.")
        return redirect("spapp:manager_settings")

# This function is to create records of model based on the post data and the given model


def create_records(req, Model):
    try:
        data = req.POST.dict()
        model = Model(data)
        if model.is_valid():
            model = Model(data).save()
            print(f"New {model} is created", model)
        messages.add_message(req, messages.SUCCESS,
                             f"You have created {model} successfully")
    except:
        messages.add_message(req, messages.WARNING,
                             "Unable to create data.")


def create_degree(req):
    create_records(req, DegreeForm)
    return redirect("spapp:manager_settings")


def create_major(req):
    create_records(req, MajorForm)
    return redirect("spapp:manager_settings")


def create_emphasis(req):
    create_records(req, EmphasisForm)
    return redirect("spapp:manager_settings")


def create_validator(req):
    print("validator called")
    data = req.POST.dict()
    exist_validator = Validator.objects.filter(email=data["email"])
    if len(exist_validator):
        print("Validator is already existed!")
        messages.add_message(req, messages.WARNING,
                             "Unable to create data, validator already existed")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    else:
        print(exist_validator, "validator not exist", data, data["email"])
    try:
        model = ValidatorForm(data)
        print(data, "reached here", model.is_valid())
        if model.is_valid():
            print("form is valid!")
            model = ValidatorForm(data).save(commit=False)
            model.created_by = req.user
            if req.user.is_staff:
                model.verified = True
            model.save()
            print(f"New {model} is created", model)
        else:
            print(model.errors)
        messages.add_message(req, messages.SUCCESS,
                         f"You have created {model} successfully")
    except:
        messages.add_message(req, messages.WARNING,
                         "Unable to create data.")
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

def delete_degree(req, pk):
    try:
        deg = Degree.objects.get(pk=pk)
        deg.delete()
    except:
        print("Deleting failed")
    return redirect("spapp:manager_settings")


def delete_major(req, pk):
    try:
        maj = Major.objects.get(pk=pk)
        maj.delete()
    except:
        print("Deleting failed")
    return redirect("spapp:manager_settings")

def delete_emphasis(req, pk):
    try:
        emp = Emphasis.objects.get(pk=pk)
        emp.delete()
    except:
        print("Deleting failed")
    return redirect("spapp:manager_settings")


def delete_validator(req, pk):
    try:
        val = Validator.objects.get(pk=pk)
        val.delete()
    except:
        print("Deleting failed")
    return redirect("spapp:manager_settings")


def edit_major(req, pk):
    cm = Major.objects.get(pk=pk)
    form = MajorForm(initial={'name': cm.name, 'degree': cm.degree})
    print(form.as_ul())
    return JsonResponse({'form': form.as_ul()})

def update_major(req):
    data = req.POST.dict()
    try:
        major = MajorForm(data)
        if major.is_valid():
            maj = Major.objects.get(pk=data["pk"])
            updated_maj = MajorForm(major.cleaned_data, instance=maj).save()
        messages.add_message(req, messages.SUCCESS, "You have successfully updated!")
    except:
        messages.add_message(req, messages.WARNING,
                            "Unable to update the current major.")
    return redirect("spapp:manager_settings")


def edit_emphasis(req, pk):
    ce = Emphasis.objects.get(pk=pk)
    form = EmphasisForm(initial={'name': ce.name, 'major': ce.major})
    print(form.as_ul())
    return JsonResponse({'form': form.as_ul()})

def update_emphasis(req):
    data = req.POST.dict()
    try:
        emphasis = EmphasisForm(data)
        if emphasis.is_valid():
            emp = Emphasis.objects.get(pk=data["pk"])
            updated_emp = EmphasisForm(emphasis.cleaned_data, instance=emp).save()
        messages.add_message(req, messages.SUCCESS, "You have successfully updated!")
    except:
        messages.add_message(req, messages.WARNING,
                            "Unable to update the current degree.")
    return redirect("spapp:manager_settings")


def edit_degree(req, pk):
    cd = Degree.objects.get(pk=pk)
    form = DegreeForm(initial={'name': cd.name, 'faculty': cd.faculty})
    print(form.as_ul())
    return JsonResponse({'form': form.as_ul()})

def update_degree(req):
    data = req.POST.dict()
    try:
        degree = DegreeForm(data)
        if degree.is_valid():
            deg = Degree.objects.get(pk=data["pk"])
            updated_deg = DegreeForm(degree.cleaned_data, instance=deg).save()
            print(deg, "Degree", degree.is_valid(), "Data", data, degree.errors.as_text)
        messages.add_message(req, messages.SUCCESS, "You have successfully updated!")
    except:
        messages.add_message(req, messages.WARNING,
                            "Unable to update the current degree.")
    return redirect("spapp:manager_settings")

 
def edit_validator(req, pk):
    cv = Validator.objects.get(pk=pk)
    form = ValidatorForm(initial={'name': cv.name, 'phone_number': cv.phone_number, 'email': cv.email, 'verified': cv.verified })
    print(form.as_ul())
    return JsonResponse({'form': form.as_ul()})

def update_validator(req):
    data = req.POST.dict()
    try:
        validator = ValidatorForm(data)
        if validator.is_valid():
            val = Validator.objects.get(pk=data["pk"])
            updated_val = ValidatorForm(validator.cleaned_data, instance=val).save()
            print(val, "validator", validator.is_valid(), "Data", data, validator.errors.as_text)
        messages.add_message(req, messages.SUCCESS, "You have successfully updated!")
    except:
        messages.add_message(req, messages.WARNING,
                            "Unable to update the current degree.")
    return redirect("spapp:manager_settings")


    

#  AR -> Activity -> Student
