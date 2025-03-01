from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import CustomUser, College,Teacher,Student,Course,Section,Subject,Department
# College Serializer
class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'

# Sub Admin Serializer
class SubAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'college', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['role'] = 'sub_admin'
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        tokens = RefreshToken.for_user(user)
        return {"access": str(tokens.access_token), "refresh": str(tokens)}

class SubjectSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField(source="course.name")
    department_name = serializers.ReadOnlyField(source="department.name")

    class Meta:
        model = Subject
        fields = ["id", "name", "code", "semester", "course", "course_name", "department", "department_name"]
class StudentSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField(source="course.name")
    department_name = serializers.ReadOnlyField(source="department.name")
    section_name = serializers.ReadOnlyField(source="section.name")
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ["id", "name", "email", "roll_number", "year", "semester", 
                  "course", "course_name", "department", "department_name", 
                  "section", "section_name", "subjects"]


class TeacherSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField(source="course.name")
    department_name = serializers.ReadOnlyField(source="department.name")
    subjects = SubjectSerializer(many=True, read_only=True)
    college_name = serializers.ReadOnlyField(source="college.name")  # ✅ College name read-only
    
    class Meta:
        model = Teacher
        fields = ["id", "name", "email", "employee_id", "qualification", "experience",
                  "college", "college_name",  # ✅ College Field Added
                  "course", "course_name", "department", "department_name", "subjects"]

    def validate_college(self, value):
        """Check if college is provided"""
        if not value:
            raise serializers.ValidationError("College is required for a teacher.")
        return value



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class SectionSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source="department.name")

    class Meta:
        model = Section
        fields = ["id", "name", "department", "department_name"]


