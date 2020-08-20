from django.db import models

# Create your models here.
class User(models.Model):
	first_name=models.CharField(max_length=15)
	last_name=models.CharField(max_length=15)

	class Meta:
		abstract=True

class Teacher(User):
	staff_no=models.IntegerField()
	type=1

	def __str__(self):
		return self.first_name+"(teacher)"

class Student(User):
	roll_no=models.IntegerField()
	type=2

	def __str__(self):
		return self.first_name+"(student)"

class Course(models.Model):
	number=models.IntegerField()
	name=models.CharField(max_length=20)

	teacher=models.ManyToManyField(Teacher, related_name="teacher")
	members=models.ManyToManyField(Student,through='StudentCourse', related_name="members")

	def __str__(self):
		return self.name

class StudentCourse(models.Model):
	approve=((0,"Pending"),(1,"Approed"))
	student=models.ForeignKey(Student,on_delete=models.CASCADE)
	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	is_approved=models.IntegerField(choices=approve)

class Assessment(models.Model):
	name=models.CharField(max_length=15)
	marks_obtained=models.IntegerField()
	total_marks=models.IntegerField()

	teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	student=models.ForeignKey(Student,on_delete=models.CASCADE)

	def __str__(self):
		percentage=round((self.marks_obtained/self.total_marks)*100,2)
		return str(self.name)+" : "+str(self.student.first_name)+" "+str(self.course.name)+"-\t"+str(percentage)