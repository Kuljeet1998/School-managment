from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
# from rest_framework import viewset
# Create your views here.

class UserList(generics.ListCreateAPIView):
	queryset=User.objects.all()
	serializer_class=UserSerializer

class TeacherList(generics.ListCreateAPIView):
	queryset=Teacher.objects.all()
	serializer_class=TeacherSerializer

class StudentList(generics.ListCreateAPIView):
	queryset=Student.objects.all()
	serializer_class=StudentSerializer

class CourseList(generics.ListCreateAPIView):
	queryset=Course.objects.all()
	serializer_class=CourseSerializer

class StudentCourseList(generics.ListCreateAPIView):
	queryset=StudentCourse.objects.all()
	serializer_class=StudentCourseSerializer

class AssessmentList(generics.ListCreateAPIView):
	queryset=Assessment.objects.all()
	serializer_class=AssessmentSerializer

class AssessmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer