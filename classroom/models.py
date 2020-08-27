from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Timestamp(models.Model):
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Teacher(Timestamp):
	staff_no=models.PositiveIntegerField(unique=True)
	user=models.OneToOneField(User ,related_name="teachers", on_delete=models.CASCADE)

	@property
	def full_name(self):
		return '{first_name} {last_name}'.format(first_name=self.user.first_name,last_name=self.user.last_name)

	def __str__(self):
		return self.full_name

class Student(Timestamp):
	roll_no=models.PositiveIntegerField(unique=True)
	user=models.OneToOneField(User ,related_name="students", on_delete=models.CASCADE)

	@property
	def full_name(self):
		return '{first_name} {last_name}'.format(first_name=self.user.first_name,last_name=self.user.last_name)

	def __str__(self):
		return self.full_name

class Course(Timestamp):
	number=models.PositiveIntegerField()
	name=models.CharField(max_length=20)

	teacher=models.ManyToManyField(Teacher, related_name="courses")
	members=models.ManyToManyField(Student,through='StudentCourse', related_name="courses")

	def __str__(self):
		return self.name

class StudentCourse(Timestamp):
	APPROVE=((0,"Pending"),(1,"Approved"))
	student=models.ForeignKey(Student,on_delete=models.CASCADE)
	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	approval_status=models.PositiveIntegerField(choices=APPROVE,default=0)

class Assessment(Timestamp):
	title=models.CharField(max_length=15)
	marks_obtained=models.PositiveIntegerField()
	total_marks=models.PositiveIntegerField()

	teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="assessments")
	course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="assessments")
	student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="assessments")

	@property
	def percentage(self):
		return round((self.marks_obtained/self.total_marks)*100,2)
	
	@property
	def full_detail(self):
		detail="{title} - STUDENT: {student} SCORED {percent}% IN  {course}".format(title=self.title,student=self.student.full_name,percent=self.percentage,course=self.course.name)
		return detail

	def __str__(self):
		return self.full_detail