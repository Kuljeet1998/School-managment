from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics, viewsets
from rest_framework import filters
# Create your views here.

#Implementing Generics View
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

#Implementing viewsets
class UserViewSet(viewsets.ModelViewSet):
	queryset=User.objects.all()
	serializer_class=UserSerializer

class TeacherViewSet(viewsets.ModelViewSet):
	queryset=Teacher.objects.all()
	filter_backends = [filters.SearchFilter,filters.OrderingFilter]
	search_fields = ['user__first_name','user__last_name','user__email']
	ordering_fields = ['staff_no']

	def get_serializer_class(self):
		if self.action=='retrieve':
			return TeacherDetailSerializer
		return TeacherSerializer


class StudentViewSet(viewsets.ModelViewSet):
	queryset=Student.objects.all()
	filter_backends = [filters.SearchFilter,filters.OrderingFilter]
	search_fields = ['user__first_name','user__last_name','user__email']
	ordering_fields = ['roll_no']

	def get_serializer_class(self):
		if self.action=='retrieve':
			return StudentDetailSerializer
		return StudentSerializer

class CourseViewSet(viewsets.ModelViewSet):
	queryset=Course.objects.all()
	serializer_class=CourseSerializer

class StudentCourseViewSet(viewsets.ModelViewSet):
	queryset=StudentCourse.objects.all()
	serializer_class=StudentCourseSerializer

class AssessmentViewSet(viewsets.ModelViewSet):
	queryset=Assessment.objects.all()
	serializer_class=AssessmentSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['student__user__first_name','teacher__user__first_name','course__name']

	def get_queryset(self):
		start=self.request.query_params.get('start',None)
		end=self.request.query_params.get('end',None)
		if start is not None:
			return Assessment.objects.filter(marks_obtained__range=(start,end))

		start_date=self.request.query_params.get('start_date',None)
		end_date=self.request.query_params.get('end_date',None)
		if start is not None:
			return Assessment.objects.filter(created__range=(start_date,end_date))
		return Assessment.objects.all()