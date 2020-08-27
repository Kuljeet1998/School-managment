from .models import *
from rest_framework import serializers
# from django.db import models


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=['id','first_name','last_name']

class TeacherSerializer(serializers.ModelSerializer):
	teacher_name=UserSerializer(read_only=True,many=True)
	class Meta:
		model=Teacher
		fields='__all__'

class StudentSerializer(serializers.ModelSerializer):
	student_name=UserSerializer(read_only=True,many=True)
	# course_details=CourseSerializer(read_only=True,many=True)
	class Meta:
		model=Student
		fields='__all__'

class CourseSerializer(serializers.ModelSerializer):
	teacher_name=TeacherSerializer(read_only=True,many=True,source='teacher')
	student_name=StudentSerializer(read_only=True,many=True,source='members')
	class Meta:
		model=Course
		fields='__all__'

class StudentCourseSerializer(serializers.ModelSerializer):

	class Meta:
		model=StudentCourse
		fields='__all__'

class AssessmentSerializer(serializers.ModelSerializer):
	class Meta:
		model=Assessment
		fields='__all__'


class StudentDetailSerializer(serializers.ModelSerializer):
	courses=serializers.StringRelatedField(many=True)
	class Meta:
		model=Student
		fields='__all__'
		depth=1

class TeacherDetailSerializer(serializers.ModelSerializer):
	courses=serializers.StringRelatedField(many=True)
	class Meta:
		model=Teacher
		fields='__all__'
		depth=1