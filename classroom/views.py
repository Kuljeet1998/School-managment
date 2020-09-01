from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework import filters
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

#Implementing viewsets
class UserViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAdminUser,)

	queryset=User.objects.all()
	serializer_class=UserSerializer

	def create(self,request):
		serializer=UserSerializer(data=request.data)
		if serializer.is_valid():
			email=request.POST.get('email')
			try:
				user = User.objects.get(email=email)
			except User.DoesNotExist:
				user = None

			if user is not None:
				return HttpResponse("Email already exists")
			else:
				serializer.save()
				return Response(serializer.data,status=201)
		return Response(serializer.errors,status=204)


class TeacherViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAdminUser,)

	queryset=Teacher.objects.all()
	filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
	search_fields = ['user__first_name','user__last_name','user__email']
	filterset_fields = ['staff_no']

	def get_serializer_class(self):
		if self.action=='retrieve' or self.action=='update':
			return TeacherDetailSerializer
		return TeacherSerializer



class StudentViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAdminUser,)

	queryset=Student.objects.all()
	filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
	search_fields = ['user__first_name','user__last_name','user__email']
	filterset_fields = ['roll_no']

	def get_serializer_class(self):
		if self.action=='retrieve' or self.action=='update':
			return StudentDetailSerializer
		return StudentSerializer
    

class CourseViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	queryset=Course.objects.all()
	serializer_class=CourseSerializer

	filter_backends = [DjangoFilterBackend]
	# search_fields = ['user__first_name','user__last_name','user__email']
	filterset_fields = ['number']

	def create(self,request):
		serializer=CourseSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		instance=serializer.save()
		members=request.data.get('members')
		teacher=request.data.get('teacher')
		instance.members.set(members)
		instance.teacher.set(teacher)
		instance.save()
		serializer=CourseSerializer(instance)
		return Response(serializer.data,status=201)

	def update(self,request):
		instance=Course.objects.get(id=pk)
		instance.number=instance.number
		instance.name=request.data.get('name',instance.name)
		members=request.data.get('members',instance.members)
		teacher=request.data.get('teacher',instance.teacher)
		instance.members.set(members)
		instance.teacher.set(teacher)
		instance.save()
		serializer=CourseSerializer(instance)
		return Response(serializer.data,status=201)

	def partial_update(self,request,pk):
		instance=Course.objects.get(id=pk)
		instance.number=instance.number
		instance.name=request.data.get('name',None)
		members=request.data.get('members',None)
		teacher=request.data.get('teacher',None)
		if members is not None:
			instance.members.set(members)
		if teacher is not None:
			instance.teacher.set(teacher)
		instance.save()
		serializer=CourseSerializer(instance)
		return Response(serializer.data,status=201)


class AssessmentViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	queryset=Assessment.objects.all()
	serializer_class=AssessmentSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['student__user__first_name','teacher__user__first_name','course__name']

	def get_queryset(self):
		marks_from=self.request.query_params.get('marks_from',None)
		marks_to=self.request.query_params.get('marks_to',None)
		if marks_from is not None and marks_to is not None:
			return Assessment.objects.filter(marks_obtained__range=(marks_from,marks_to))

		start_date=self.request.query_params.get('start_date',None)
		end_date=self.request.query_params.get('end_date',None)
		if start_date is not None and end_date is not None:
			return Assessment.objects.filter(created__range=(start_date,end_date))
		
		return Assessment.objects.all()


class MeAPI(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)


	def get(self,request):
		user=self.request.user
		is_teacher=False
		is_student=False
		is_teacher=Teacher.objects.filter(user_id=user.id).exists()
		is_student=Student.objects.filter(user_id=user.id).exists()

		if is_teacher==True and is_student==False:
			
			teacher=Teacher.objects.get(user_id=user.id)
			serializer=TeacherDetailSerializer(teacher)
			serializer_data=serializer.data
			serializer_data['user_type']="Teacher"
			return Response(serializer_data,status=201)

		elif is_student==True and is_teacher==False:
			student=Student.objects.get(user_id=user.id)
			serializer=StudentDetailSerializer(student)
			serializer_data=serializer.data
			serializer_data['user_type']="Student"
			return Response(serializer_data,status=201)

		elif is_student==True and is_teacher==True:
			teacher=Teacher.objects.get(user_id=user.id)
			serializer1=TeacherDetailSerializer(teacher)
			student=Student.objects.get(user_id=user.id)
			serializer2=StudentDetailSerializer(student)

			serializer1_data=serializer1.data
			serializer2_data=serializer2.data
			serializer1_data['courses_learning']=serializer1_data.pop('courses')
			serializer2_data['courses_taught']=serializer2_data.pop('courses')

			serializer2_data.update(serializer1_data)
			serializer2_data['user_type']="Both"
			return Response(serializer2_data, status=201)

		else:
			return Response("You are admin !")