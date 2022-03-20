from django import forms

from .models import (AcademicRecognition, Activity, CommunityService, Degree,
                     Emphasis, Internship, Job, Major, PreviousJob, Project,
                     Research, Student, Validator)


class StudentForm(forms.ModelForm):
    # user = forms.CharField(widget=forms.TextInput(
    #     attrs={
    #         'type': 'hidden',
    #         }
    #     ))
    # date_of_birth = forms.CharField(widget=forms.TextInput(
    #     attrs={
    #         'type': 'date',
    #         }
    #     ))

    nationality = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'text',
            'placeholder': 'Khmer',
            'class': ""
        }
    ))

    class Meta:
        model = Student
        fields = ['interests',  'nationality']

# Activity Form
class ActivityForm(forms.ModelForm):
    from_date = forms.DateField(widget=forms.DateInput(
        attrs={
             'type': 'date',
            }
    )) 

    to_date = forms.DateField(widget=forms.DateInput(
        attrs={
             'type': 'date',
            }
    ))
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ('verification_status', 'rewarded_points', 'activity_name', 'student', )
  
# Project Form
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('activity',)

# Research Form
class ResearchForm(forms.ModelForm):
    published_date = forms.DateField(widget=forms.DateInput(
        attrs={
             'type': 'date',
            }
    )) 


    class Meta:
        model = Research
        fields = '__all__'
        exclude = ('activity',)


# Internship Form
class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = '__all__'
        exclude = ('activity',)

# PreviousJob Form
class PJForm(forms.ModelForm):
    class Meta:
        model = PreviousJob
        fields = '__all__'
        exclude = ('activity',)


# CommunityService Form
class CSForm(forms.ModelForm):
    class Meta:
        model = CommunityService
        fields = '__all__'
        exclude = ('activity',)


# academic recognition
class ARForm(forms.ModelForm):
    class Meta:
        model = AcademicRecognition
        fields = '__all__'
        exclude = ('activity',)


class DegreeForm(forms.ModelForm):
    class Meta:
        model = Degree
        fields = '__all__'


class MajorForm(forms.ModelForm):
    class Meta:
        model = Major
        fields = '__all__'


class EmphasisForm(forms.ModelForm):
    class Meta:
        model = Emphasis
        fields = '__all__'


class ValidatorForm(forms.ModelForm):
    class Meta:
        model = Validator
        fields = "__all__"
        exclude = ["created_by", "verified"]

class JobForm(forms.ModelForm):
    class Meta:
        model = Emphasis
        fields = '__all__'
