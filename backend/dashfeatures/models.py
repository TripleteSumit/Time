from django.db import models
from django.conf import settings


# Create your models here.
class Semestar(models.Model):
    name = models.CharField(max_length=255)


class Department(models.Model):
    COMPUTER_SCIENCE = 'CSE'
    ELECTRICAL = 'EEE'
    MECHANICAL = 'MECH'
    ELECTRONIC = 'ECE'
    AGRICULTURE = 'AG'
    DEPARTMENT_CHOICES = [
        (COMPUTER_SCIENCE, 'COMPUTER SCIENCE AND ENGINEERING'),
        (ELECTRICAL, 'ELECTRICAL ENGINEERING'),
        (MECHANICAL, 'MECHANICAL ENGINEERING'),
        (ELECTRONIC, 'ELECTRONIC AND COMMUNICATION ENGINEERING'),
        (AGRICULTURE, 'AGRICULTURE ENGINEERING')
    ]
    name = models.CharField(max_length=255, choices=DEPARTMENT_CHOICES)


class Section(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)


class Student(models.Model):
    regd_no = models.CharField(primary_key=True, unique=True, max_length=255)
    name = models.CharField(max_length=255)
    roll_no = models.SmallIntegerField()
    section = models.ForeignKey(Section, on_delete=models.PROTECT)
    semestar = models.ForeignKey(Semestar, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


class Subject(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semestar = models.ForeignKey(Semestar, on_delete=models.CASCADE)


class Teacher(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=12)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject)


class Attendance(models.Model):
    date = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
