from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.dispatch import receiver  # Correct import for receiver
from django.db.models.signals import post_save


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        super().save(*args, **kwargs)


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)


class Student(User):
    base_role = User.Role.STUDENT
    student = StudentManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "only for students"

@receiver(post_save, sender=Student)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'STUDENT':
        StudentProfile.objects.create(user=instance)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(null=True, blank=True)  # Corrected typo


class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.TEACHER)


class Teacher(User):
    base_role = User.Role.TEACHER
    teacher = TeacherManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "only for Teachers"


@receiver(post_save, sender=Teacher)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'TEACHER':
        TeacherProfile.objects.create(user=instance)

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.IntegerField(null=True, blank=True)  # Corrected typo
