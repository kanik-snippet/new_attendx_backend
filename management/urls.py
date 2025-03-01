from django.urls import path
from .views import *

urlpatterns = [
    path("generate-qr/", generate_qr, name="generate_qr"),
    path("mark-attendance/", mark_attendance, name="mark_attendance"),
    path('create-lecture/',create_lecture,name='create-lecture'),





    path('login/', LoginAPIView.as_view(), name='login'),
    path('colleges/create/', CreateCollegeAPIView.as_view(), name='create-college'),
    path('colleges/', ListCollegesAPIView.as_view(), name='list-colleges'),

    # ✅ Super Admin: Sub Admin Management
    path('sub-admins/create/', CreateSubAdminAPIView.as_view(), name='create-sub-admin'),
    path('sub-admins/', ListSubAdminsAPIView.as_view(), name='list-sub-admins'),
    path('sub-admins/<int:pk>/', RetrieveSubAdminAPIView.as_view(), name='retrieve-sub-admin'),
    path('sub-admins/<int:pk>/update/', UpdateSubAdminAPIView.as_view(), name='update-sub-admin'),
    path('sub-admins/<int:pk>/delete/', DeleteSubAdminAPIView.as_view(), name='delete-sub-admin'),

    # ✅ Sub Admin: Student Management
    path('students/create/', CreateStudentAPIView.as_view(), name='create-student'),
    path('students/', ListStudentsAPIView.as_view(), name='list-students'),
    path('students/<int:pk>/', RetrieveStudentAPIView.as_view(), name='retrieve-student'),
    path('students/<int:pk>/update/', UpdateStudentAPIView.as_view(), name='update-student'),
    path('students/<int:pk>/delete/', DeleteStudentAPIView.as_view(), name='delete-student'),

    # ✅ Sub Admin: Teacher Management
    path('teachers/create/', CreateTeacherAPIView.as_view(), name="create_teacher"),
    path('teachers/', ListTeachersAPIView.as_view(), name="list_teachers"),
    path('teachers/<int:pk>/', RetrieveTeacherAPIView.as_view(), name="retrieve_teacher"),
    path('teachers/<int:pk>/update/', UpdateTeacherAPIView.as_view(), name="update_teacher"),
    path('teachers/<int:pk>/delete/', DeleteTeacherAPIView.as_view(), name="delete_teacher"),

    # ✅ Sub Admin: Course Management
    path('courses/', ListCoursesAPIView.as_view(), name="list_courses"),
    path('courses/create/', CreateCourseAPIView.as_view(), name="create_course"),
    path('courses/<int:pk>/', RetrieveCourseAPIView.as_view(), name="retrieve_course"),
    path('courses/<int:pk>/update/', UpdateCourseAPIView.as_view(), name="update_course"),
    path('courses/<int:pk>/delete/', DeleteCourseAPIView.as_view(), name="delete_course"),

    # ✅ Sub Admin: Department Management
    path('departments/', ListDepartmentsAPIView.as_view(), name="list_departments"),
    path('departments/create/', CreateDepartmentAPIView.as_view(), name="create_department"),
    path('departments/<int:pk>/', RetrieveDepartmentAPIView.as_view(), name="retrieve_department"),
    path('departments/<int:pk>/update/', UpdateDepartmentAPIView.as_view(), name="update_department"),
    path('departments/<int:pk>/delete/', DeleteDepartmentAPIView.as_view(), name="delete_department"),

    # ✅ Sub Admin: Subject Management
    path('subjects/', ListSubjectsAPIView.as_view(), name="list_subjects"),
    path('subjects/create/', CreateSubjectAPIView.as_view(), name="create_subject"),
    path('subjects/<int:pk>/', RetrieveSubjectAPIView.as_view(), name="retrieve_subject"),
    path('subjects/<int:pk>/update/', UpdateSubjectAPIView.as_view(), name="update_subject"),
    path('subjects/<int:pk>/delete/', DeleteSubjectAPIView.as_view(), name="delete_subject"),
 
    # ✅ Sub Admin: Section Management
    path('sections/create/', CreateSectionAPIView.as_view(), name='create-section'),
    path('sections/', ListSectionsAPIView.as_view(), name='list-sections'),
    path('sections/<int:pk>/', RetrieveSectionAPIView.as_view(), name='retrieve-section'),
    path('sections/<int:pk>/update/', UpdateSectionAPIView.as_view(), name='update-section'),
    path('sections/<int:pk>/delete/', DeleteSectionAPIView.as_view(), name='delete-section'),
]
