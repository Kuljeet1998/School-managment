from django.test import TestCase
from classroom.models import *
from django.contrib.auth.models import User
# import unittest
# Create your tests here.

class UserTestCase(TestCase):

	def setUp(self):
		user=User.objects.create_user('foo', password='bar')
		user.is_superuser=False
		user.is_staff=True
		user.save()
		user=User.objects.first()


	def test_display_user(self):
		user=User.objects.get(username="foo")
		print(user)	
		self.assertEqual(user.username,"foo")




class AssessmentTestCase(TestCase):

	def setUp(self):
		user=User.objects.create_user('foo', password='bar')
		user.is_superuser=False
		user.is_staff=True
		user.save()
		user=User.objects.first()

		Teacher.objects.create(staff_no=1,user=user)
		Student.objects.create(roll_no=1,user=user)

		teacher=Teacher.objects.first()
		student=Student.objects.first()

		Course.objects.create(number=1,name="TEST COURSE")
		course=Course.objects.first()
		course.teacher.add(teacher)
		StudentCourse.objects.create(student=student,course=course,is_approved=1)
		course.members.add(student)

		Assessment.objects.create(title="Sem1", marks_obtained=14, total_marks=20,teacher=teacher,student=student,course=course)
		Assessment.objects.create(title="Sem2",marks_obtained=12,total_marks=20,teacher=teacher,student=student,course=course)

	def test_display_percent(self):
		sem1=Assessment.objects.get(title="Sem1")
		sem2=Assessment.objects.get(title="Sem2")
		print(sem1)
		print(sem2)
		title1=sem1.title
		title2=sem2.title
		print(title1+"  \t "+ title2)
		self.assertEqual(title1, 'Sem1')
		self.assertEqual(title2, 'Sem2')