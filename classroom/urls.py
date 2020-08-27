from django.urls import path
from .views import *
from classroom import views
from rest_framework import routers
#Calling generic Views
# urlpatterns=[
# 	path('user/',views.UserList.as_view()),
# 	path('student/',views.StudentList.as_view()),
# 	path('teacher/',views.TeacherList.as_view()),
# 	path('course/',views.CourseList.as_view()),
# 	path('student_course/',views.StudentCourseList.as_view()),
# 	path('assessment/',views.AssessmentList.as_view()),
# 	path('assessment/<int:pk>/',views.AssessmentDetail.as_view()),
# ]

#Implementing routers
router=routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'student', StudentViewSet)
router.register(r'course', CourseViewSet)
router.register(r'student_course', StudentCourseViewSet)
router.register(r'assessment', AssessmentViewSet)
urlpatterns=router.urls