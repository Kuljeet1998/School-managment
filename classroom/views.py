from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics, viewsets
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
		if self.action=='retrieve':
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
		if self.action=='retrieve':
			return StudentDetailSerializer
		return StudentSerializer
    

class CourseViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	queryset=Course.objects.all()
	serializer_class=CourseSerializer


class AssessmentViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	queryset=Assessment.objects.all()
	serializer_class=AssessmentSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['student__user__first_name','teacher__user__first_name','course__name']

	def get_queryset(self):
		start=self.request.query_params.get('start',None)
		end=self.request.query_params.get('end',None)
		if start is not None and end is not None:
			return Assessment.objects.filter(marks_obtained__range=(start,end))

		start_date=self.request.query_params.get('start_date',None)
		end_date=self.request.query_params.get('end_date',None)
		if start_date is not None and end_date is not None:
			return Assessment.objects.filter(created__range=(start_date,end_date))
		return Assessment.objects.all()


# class MeAPIViewSet(viewsets.ModelViewSet):
# 	authentication_classes = (TokenAuthentication,)
# 	permission_classes = (IsAuthenticated,)

# 	is_teacher=False
# 	is_student=False
# 	def get_queryset(self):
# 		user=self.request.user
# 		import pdb;
# 		pdb.set_trace()
# 		is_teacher=Teacher.objects.filter(user_id=user.id).exists()
# 		is_student=Student.objects.filter(user_id=user.id).exists()

# 		if is_teacher==True and is_student==False:
# 			return Teacher.objects.filter(user_id=user.id)

# 		elif is_student==True and is_teacher==False:
# 			return Student.objects.filter(user_id=user.id)

# 		else:
# 			return Teacher.objects.filter(user_id=user.id) , Student.objects.filter(user_id=user.id)

