from django.urls import path
from .views import *
from classroom import views
urlpatterns=[
	path('user/',views.UserList.as_view()),
	path('student/',views.StudentList.as_view()),
	path('teacher/',views.TeacherList.as_view()),
	path('course/',views.CourseList.as_view()),
	path('student_course/',views.StudentCourseList.as_view()),
	path('assessment/',views.AssessmentList.as_view()),
	path('assessment/<int:pk>/',views.AssessmentDetail.as_view()),
]