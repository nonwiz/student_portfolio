from .models import Student, Degree, Major, Emphasis, Validator, AcademicRecognition
from django import forms


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
        fields = ['email', 'phone_number', 'name']
