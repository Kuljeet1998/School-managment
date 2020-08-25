from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Teacher(models.Model):
	staff_no=models.IntegerField(primary_key=True)
	user=models.OneToOneField(User ,related_name="teacher", on_delete=models.CASCADE)


	def __str__(self):
		return self.user.first_name+" (teacher)"

class Student(models.Model):
	roll_no=models.IntegerField(primary_key=True)
	user=models.OneToOneField(User ,related_name="student", on_delete=models.CASCADE)


	def __str__(self):
		return self.user.first_name+" (student)"

class Course(models.Model):
	number=models.IntegerField()
	name=models.CharField(max_length=20)

	teacher=models.ManyToManyField(Teacher, related_name="course")
	members=models.ManyToManyField(Student,through='StudentCourse', related_name="course")

	def __str__(self):
		return self.name

class StudentCourse(models.Model):
	APPROVE=((0,"Pending"),(1,"Approved"))
	student=models.ForeignKey(Student,on_delete=models.CASCADE)
	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	is_approved=models.IntegerField(choices=APPROVE,default=0)

class Assessment(models.Model):
	title=models.CharField(max_length=15)
	marks_obtained=models.IntegerField()
	total_marks=models.IntegerField()

	teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="assessment")
	course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="assessment")
	student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="assessment")

	def __str__(self):
		percentage=round((self.marks_obtained/self.total_marks)*100,2)
		return str(self.title)+" : "+str(self.student.user.first_name)+" "+str(self.course.name)+"-\t"+str(percentage)