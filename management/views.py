import qrcode
from io import BytesIO
import base64
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils.timezone import now
from .models import *
from .permissions import IsSuperAdmin,IsSuperAdminOrSubAdmin  # ✅ Importing Custom Permission
from .serializers import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# ✅ Bearer Token Parameter for Swagger
token_param = openapi.Parameter(
    'Authorization',
    in_=openapi.IN_HEADER,
    description="JWT Bearer Token (Format: Bearer <your_token>)",
    type=openapi.TYPE_STRING,
    required=True
)

class LoginAPIView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
# ✅ Create College API
class CreateCollegeAPIView(generics.CreateAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    permission_classes = [IsAuthenticated,IsSuperAdmin]

    @swagger_auto_schema(
        manual_parameters=[token_param],  # Bearer Token Field Added
        operation_description="Super Admin can create colleges",
        responses={201: CollegeSerializer, 400: "Bad Request"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# ✅ Create Sub Admin API
class CreateSubAdminAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.filter(role="sub_admin")
    serializer_class = SubAdminSerializer
    permission_classes = [IsAuthenticated,IsSuperAdmin]

    @swagger_auto_schema(
        manual_parameters=[token_param],  # Bearer Token Field Added
        operation_description="Super Admin can create Sub Admins for a specific college",
        responses={201: SubAdminSerializer, 400: "Bad Request"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# ✅ List Colleges API
class ListCollegesAPIView(generics.ListAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    permission_classes = [IsAuthenticated,IsSuperAdmin]

    @swagger_auto_schema(
        manual_parameters=[token_param],  # Bearer Token Field Added
        operation_description="Super Admin can list all colleges",
        responses={200: CollegeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class ListSubAdminsAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role="sub_admin")
    serializer_class = SubAdminSerializer
    permission_classes = [IsAuthenticated,IsSuperAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin can view all Sub Admins",
        manual_parameters=[token_param],  # Bearer Token Field Added

        responses={200: SubAdminSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class RetrieveSubAdminAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.filter(role="sub_admin")
    serializer_class = SubAdminSerializer
    permission_classes = [IsAuthenticated,IsSuperAdmin]

    @swagger_auto_schema(
        operation_description="Get details of a specific Sub Admin",
        manual_parameters=[token_param],  # Bearer Token Field Added

        responses={200: SubAdminSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UpdateSubAdminAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.filter(role="sub_admin")
    serializer_class = SubAdminSerializer
    permission_classes = [IsAuthenticated,IsSuperAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin can update Sub Admin details",
        manual_parameters=[token_param],  # Bearer Token Field Added

        responses={200: SubAdminSerializer, 400: "Bad Request"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

class DeleteSubAdminAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.filter(role="sub_admin")
    serializer_class = SubAdminSerializer
    permission_classes = [IsAuthenticated,IsSuperAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin can delete a Sub Admin",
        manual_parameters=[token_param],  # Bearer Token Field Added

        responses={204: "No Content"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class CreateStudentAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can create students",
        manual_parameters=[token_param],  # Bearer Token Field Added
        responses={201: StudentSerializer, 400: "Bad Request"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# ✅ List Students API
class ListStudentsAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can list students",
        manual_parameters=[token_param],  
        responses={200: StudentSerializer(many=True), 400: "Bad Request"}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# ✅ Retrieve Student API
class RetrieveStudentAPIView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can retrieve student details",
        manual_parameters=[token_param],  
        responses={200: StudentSerializer, 404: "Not Found"}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# ✅ Update Student API
class UpdateStudentAPIView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can update student details",
        manual_parameters=[token_param],  
        responses={200: StudentSerializer, 400: "Bad Request"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

# ✅ Delete Student API
class DeleteStudentAPIView(generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can delete a student",
        manual_parameters=[token_param],  
        responses={204: "No Content", 400: "Bad Request"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class CreateTeacherAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.filter(role="teacher")
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]  

    @swagger_auto_schema(
        operation_description="Sub Admin can create teachers",
        manual_parameters=[token_param],
        responses={201: TeacherSerializer, 400: "Bad Request"}
    )
    def post(self, request, *args, **kwargs):
        """Custom handling to prevent duplicate email/username issues"""
        email = request.data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)


class ListTeachersAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role="teacher")
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]  

    @swagger_auto_schema(
        operation_description="Sub Admin can list all teachers",
        manual_parameters=[token_param],
        responses={200: TeacherSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RetrieveTeacherAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.filter(role="teacher")
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]  

    @swagger_auto_schema(
        operation_description="Sub Admin can retrieve a specific teacher",
        manual_parameters=[token_param],
        responses={200: TeacherSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UpdateTeacherAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.filter(role="teacher")
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]  
    http_method_names = ["patch"]  # ✅ PATCH instead of PUT

    @swagger_auto_schema(
        operation_description="Sub Admin can update teacher details (partial update supported)",
        manual_parameters=[token_param],
        responses={200: TeacherSerializer, 400: "Bad Request"}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class DeleteTeacherAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.filter(role="teacher")
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]  

    @swagger_auto_schema(
        operation_description="Sub Admin can delete a teacher",
        manual_parameters=[token_param],
        responses={204: "Teacher deleted successfully"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

#course API
class CreateCourseAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can create a course",
        manual_parameters=[token_param],
        responses={201: CourseSerializer, 400: "Bad Request"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ListCoursesAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can list all courses",
        manual_parameters=[token_param],
        responses={200: CourseSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RetrieveCourseAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can retrieve a specific course",
        manual_parameters=[token_param],
        responses={200: CourseSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UpdateCourseAPIView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can update a course",
        manual_parameters=[token_param],
        responses={200: CourseSerializer, 400: "Bad Request"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class DeleteCourseAPIView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can delete a course",
        manual_parameters=[token_param],
        responses={204: "Course deleted successfully"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

#Department Apis
class CreateDepartmentAPIView(generics.CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can create a department",
        manual_parameters=[token_param],
        responses={201: DepartmentSerializer, 400: "Bad Request"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ListDepartmentsAPIView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can list all departments",
        manual_parameters=[token_param],
        responses={200: DepartmentSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RetrieveDepartmentAPIView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can retrieve a specific department",
        manual_parameters=[token_param],
        responses={200: DepartmentSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UpdateDepartmentAPIView(generics.UpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can update a department",
        manual_parameters=[token_param],
        responses={200: DepartmentSerializer, 400: "Bad Request"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class DeleteDepartmentAPIView(generics.DestroyAPIView):
    queryset = Department.objects.all()
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can delete a department",
        manual_parameters=[token_param],
        responses={204: "Department deleted successfully"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

#Subject Apis
class CreateSubjectAPIView(generics.CreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can create a subject",
        manual_parameters=[token_param],
        responses={201: SubjectSerializer, 400: "Bad Request"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ListSubjectsAPIView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can list all subjects",
        manual_parameters=[token_param],
        responses={200: SubjectSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RetrieveSubjectAPIView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can retrieve a specific subject",
        manual_parameters=[token_param],
        responses={200: SubjectSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UpdateSubjectAPIView(generics.UpdateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can update a subject",
        manual_parameters=[token_param],
        responses={200: SubjectSerializer, 400: "Bad Request"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class DeleteSubjectAPIView(generics.DestroyAPIView):
    queryset = Subject.objects.all()
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Super Admin or Sub Admin can delete a subject",
        manual_parameters=[token_param],
        responses={204: "Subject deleted successfully"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class CreateSectionAPIView(generics.CreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Sub Admin can create sections",
        manual_parameters=[token_param],
        responses={201: SectionSerializer, 400: "Bad Request"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ListSectionsAPIView(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Sub Admin can list all sections",
        manual_parameters=[token_param],
        responses={200: SectionSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class RetrieveSectionAPIView(generics.RetrieveAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Sub Admin can retrieve a specific section",
        manual_parameters=[token_param],
        responses={200: SectionSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UpdateSectionAPIView(generics.UpdateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Sub Admin can update section details",
        manual_parameters=[token_param],
        responses={200: SectionSerializer, 400: "Bad Request"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

class DeleteSectionAPIView(generics.DestroyAPIView):
    queryset = Section.objects.all()
    permission_classes = [IsAuthenticated, IsSuperAdminOrSubAdmin]

    @swagger_auto_schema(
        operation_description="Sub Admin can delete a section",
        manual_parameters=[token_param],
        responses={204: "Section deleted successfully"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

import qrcode
import base64
import json
from io import BytesIO
from django.utils.timezone import now
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Lecture

def generate_qr(request, lecture_id):
    # Lecture Fetch Karo
    lecture = get_object_or_404(Lecture, id=lecture_id)

    # QR Code Expiry Time (5 min)
    expiry_time = now() + timedelta(minutes=5)
    lecture.qr_expiry = expiry_time
    lecture.save()

    # QR Code Data (Lecture ID + Expiry)
    qr_data = json.dumps({"lecture_id": lecture.id, "expires_at": expiry_time.isoformat()})
    
    # QR Code Generate
    qr = qrcode.make(qr_data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return JsonResponse({"qr_code": qr_base64, "expires_at": expiry_time})

import json
import base64
from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.shortcuts import get_object_or_404
from .models import Attendance, AttendanceRecord, Lecture

@csrf_exempt
def mark_attendance(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Student se QR Code + Location lo
            qr_data = data.get("qr_data")
            student_lat = float(data.get("latitude", 0))
            student_lon = float(data.get("longitude", 0))

            # QR Code decode karo
            decoded_data = base64.b64decode(qr_data).decode("utf-8")
            qr_json = json.loads(decoded_data)

            # Lecture ID & expiry check karo
            lecture_id = qr_json.get("lecture_id")
            expires_at = qr_json.get("expires_at")

            if now().isoformat() > expires_at:
                return JsonResponse({"message": "QR Code expired!"}, status=400)

            # Lecture fetch karo
            lecture = get_object_or_404(Lecture, id=lecture_id)

            # Teacher aur Student location compare karo
            teacher_location = Point(lecture.location.x, lecture.location.y, srid=4326)
            student_location = Point(student_lat, student_lon, srid=4326)

            if teacher_location.distance(student_location) > D(m=50):
                status = "proxy"
            else:
                status = "present"

            # Attendance Record Save Karo
            attendance, created = Attendance.objects.get_or_create(lecture=lecture, defaults={"status": "open"})
            AttendanceRecord.objects.create(attendance=attendance, student=request.user, status=status)

            return JsonResponse({"message": "Attendance marked!", "status": status})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method"}, status=400)

from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import Point
import json
from .models import Lecture

@csrf_exempt
def create_lecture(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Teacher, Course, Department, Section, Location lo
            teacher = request.user
            course_id = data.get("course_id")
            department_id = data.get("department_id")
            section_id = data.get("section_id")
            teacher_lat = float(data.get("latitude", 0))
            teacher_lon = float(data.get("longitude", 0))

            # Start Time Abhi Ka Set Karo
            start_time = now()

            # Lecture Create Karo
            lecture = Lecture.objects.create(
                teacher=teacher,
                course_id=course_id,
                department_id=department_id,
                section_id=section_id,
                start_time=start_time,
                location=Point(teacher_lat, teacher_lon, srid=4326),
                status="open"
            )

            return JsonResponse({"message": "Lecture created!", "lecture_id": lecture.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method"}, status=400)

