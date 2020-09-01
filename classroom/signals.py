# from django.contrib.auth.models import *
# from django.db.models.signals import post_save,pre_save,m2m_changed
# from django.dispatch import receiver
# from .models import *
# from rest_framework.response import Response

# @receiver(post_save,sender=Course)
# def on_save(sender,instance:Course,**kwargs):
	
# 	previous_course_object=Course.objects.get(id=instance.id)
	
# 	previous_members=previous_course_object.members
# 	new_members=instance.members
	
# 	import pdb;
# 	pdb.set_trace()
# 	for members in new_members.all():
# 		if members not in previous_members:
# 			new_student_list.append(members)

# 	for members in new_student_list:
# 		student=Student.objects.get(id=members)
# 		StudentCourse.objects.create(student=student,course=instance)