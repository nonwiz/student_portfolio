from django.contrib.auth.models import User
from django.db import models
# from django.db.models.fields import related
from django.urls import reverse


class Degree(models.Model):
    name = models.CharField(max_length=40)
    faculty = models.CharField(max_length=50)

    """ the __str__ function overides the name of an object and displays it as a string """

    def __str__(self):
        """ the 'f' before the string, allows you to include varibles in your string, which should 
            be inclosed in curly braces {} """
        return f"{self.name}"


class Major(models.Model):
    """ the ForeignKey creates a relatioship between the degree table (parent) and the Major table (child)
        on_delete, will delete the child, if the parent is deleted
    """
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"


class Emphasis(models.Model):
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=10, unique=True, null=True)
    date_of_birth = models.DateField(null=True)
    nationality = models.CharField(max_length=30, null=True)
    major = models.ForeignKey(Major, on_delete=models.CASCADE, null=True)
    bio_char = models.CharField(max_length=200, null=True)
    interests = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=12, null=True)
    image = models.ImageField(
        upload_to='theme/static/user_image', null=True, default="theme/static/user_image/default-image.png")
    website = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"student: {self.user}, nationality: {self.nationality}, dob: {self.date_of_birth}, Interests: {self.interests}, bio_char: {self.bio_char}"

    def get_absolute_url(self):
        return reverse('spapp:setting', kwargs={'pk': self.user.id})


class Validator(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.email}"


class Activity(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=30, null=True)
    description = models.TextField(null=True)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    validator = models.ForeignKey(
        Validator, null=True, on_delete=models.SET_NULL)
    verification_status = models.BooleanField(default=False)
    #approved_by_manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    rewarded_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student} {self.activity_name} {self.description} | {self.validator} {self.verification_status}"


class AcademicRecognition(models.Model):
    SEMESTER = [('first_semester', 'First Semester'),
                ('second_semester', 'Second Semester')]
    activity = models.OneToOneField(
        Activity, on_delete=models.CASCADE, related_name="academic_recognition")
    semester = models.CharField(max_length=30, choices=SEMESTER)
    gpa = models.FloatField(max_length=3)
    year = models.IntegerField(default=2015)

    def __str__(self):
        return f"{self.activity.student} has {self.gpa} @ {self.semester}, {self.year}"


class CommunityService(models.Model):
    activity = models.OneToOneField(
        Activity, on_delete=models.CASCADE, related_name="community_service")
    location = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.activity.student} - {self.activity.description} at {self.location}"


class Project(models.Model):
    activity = models.OneToOneField(
        Activity, on_delete=models.CASCADE, related_name="project")
    resonsibility = models.TextField()
    location = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.activity.student} - {self.activity.description}"


class Research(models.Model):
    activity = models.OneToOneField(
        Activity, on_delete=models.CASCADE, related_name="research")
    co_authors = models.CharField(max_length=100, null=True)
    link = models.CharField(max_length=50, null=True)
    published_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.activity.student} - {self.activity.description}"


class Internship(models.Model):
    activity = models.OneToOneField(
        Activity, on_delete=models.CASCADE, related_name="internship")

    def __str__(self):
        return f"{self.activity.student} - {self.activity.description}"


class PreviousJob(models.Model):
    activity = models.OneToOneField(
        Activity, on_delete=models.CASCADE, related_name="previous_job")

    def __str__(self):
        return f"{self.activity.student} - {self.activity.description}"


class Job(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True)
    location = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=20, null=True)
    website = models.CharField(max_length=90, null=True)
    posted = models.DateField(auto_now_add=True)
    type = models.CharField(default="Full Time", max_length=50)
    company_name = models.CharField(default="", max_length=50)

    def __str__(self):
        return f"{self.title}, {self.location}"


class AccountRemovalRequest(models.Model):
    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, related_name="account_removal_request")
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.first_name}, Requested: {self.date}, Status: {self.status}"


"""

Plan for Backend:
Student:
- updating personal profile
- registering should show the username of the user 
- if forgotten, maybe create a function to return the username with given email address.
- Request to delete personal information
- Request to add activity
- convert student profile to resume or pdf format

Managers (SA):
- Adding Major and Degree: CRUD
- to manage student accounts
- Update students activity request
- Erase studnet's information (profile)
- Generate log when making operation like Major / Verify

Superuser:
1 Superuser > Multiple Manager (Registrar / SA) > Student

Feb:
Wk1: Summary / Database Checking / Planning
Wk2: Registration of user / updating personal profile / if forgotten password will show / request to delete personal info / CRUD major and degree / Student Account
Wk3: requests to add activity
Wk4:

March:
Wk1:
Wk2:
Wk3:
Wk4:

"""
