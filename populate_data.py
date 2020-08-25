import os,random
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE",'school2.settings')
django.setup()
from django.contrib.auth.models import User
from faker import Faker
from classroom.models import *


def create_course(N):
	faker=Faker()
	for _ in range(N):
		x=random.randint(1,4)
		name=faker.name()
		a1=Course(number=x,name=name)
		a1.save()
		number_of_attachment=random.randint(1,4)
		for y in range(1,number_of_attachment+1):
			a1.teacher.add(y)


def create_studentcourse(N):
	faker=Faker()
	student_limit=Student.objects.all().count()
	course_limit=Course.objects.all().count()
	for _ in range(N):
		std_id=random.randint(1,student_limit)
		course_id=random.randint(1,course_limit)
		approval=random.randint(1,2)

		
		if(Course.objects.filter(id=course_id).exists()):
			student_obj=Student.objects.get(roll_no=std_id)
			course_obj=Course.objects.get(id=course_id)
			a1=StudentCourse(student=student_obj,course=course_obj,is_approved=approval)
			a1.save()

def create_assessment(N):
	faker=Faker()
	title=faker.name()
	
	total_marks=20
	
	teacher_limit=Teacher.objects.all().count()
	student_limit=Student.objects.all().count()
	course_limit=Course.objects.all().count()

	for _ in range(N):
		marks_obtained=random.randint(0,20)
		teacher_id=random.randint(1,teacher_limit)
		student_id=random.randint(1,student_limit)
		course_id=random.randint(1,course_limit)

		if(Teacher.objects.filter(staff_no=teacher_id).exists() and Student.objects.filter(roll_no=student_id).exists() and Course.objects.filter(id=course_id)):
			
			teacher_obj=Teacher.objects.get(staff_no=teacher_id)
			student_obj=Student.objects.get(roll_no=student_id)
			course_obj=Course.objects.get(id=course_id)
			a=Assessment(title=title,marks_obtained=marks_obtained,total_marks=total_marks,teacher=teacher_obj,course=course_obj,student=student_obj)
			a.save()

create_course(2)
create_studentcourse(2)
create_assessment(2)