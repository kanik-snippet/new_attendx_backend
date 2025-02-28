from django.contrib.auth.models import AbstractUser
from django.db import models

# College Model
class College(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Course(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.college.name})"

class Department(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.course.name})"

class Section(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=50)  # Example: A, B, C

    def __str__(self):
        return f"Section {self.name} ({self.department.name})"


# Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('sub_admin', 'Sub Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")

    def __str__(self):
        return f"{self.username} - {self.role}"

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subjects",null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="subjects")

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)  # Example: "CS101"
    semester = models.IntegerField()  # ✅ Example: 1st sem, 2nd sem

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.department.name}, {self.course.name}"

class Student(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    roll_number = models.CharField(max_length=50, unique=True)
    year = models.IntegerField()  # ✅ Example: 1st year, 2nd year
    semester = models.IntegerField()  # ✅ Example: 1st sem, 2nd sem
    subjects = models.ManyToManyField(Subject, related_name="students")  # ✅ Subjects Assigned

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number}) - {self.department.name}, {self.course.name}, {self.college.name}"


class Teacher(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    employee_id = models.CharField(max_length=50, unique=True)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    subjects = models.ManyToManyField(Subject, related_name="teachers")  # ✅ Subjects Assign

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.employee_id}) - {self.department.name}"





    