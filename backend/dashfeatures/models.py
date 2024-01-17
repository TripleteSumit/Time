from django.db import models
from django.conf import settings


# Create your models here.
class Semestar(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


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

    def __str__(self) -> str:
        return self.name


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

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class Teacher(models.Model):
    phone_no = models.CharField(max_length=12)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'


class Attendance(models.Model):
    date = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
