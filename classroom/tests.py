from django.test import TestCase

# Create your tests here.
class AssessmentTestCase(TestCase):
	def setup(self):
		Assessment.objects.create(title="Sem1", marks_obtained=14, total_marks=20,teacher=Teacher.objects.get(id=2),student=Student.objects.get(id=1),course=Course.objects.get(id=3))
		Assessment.objects.create(title="Sem2",marks_obtained=12,total_marks=20,teacher=Teacher.objects.get(id=2),student=Student.objects.get(id=1),course=Course.objects.get(id=3))

	def display_percent(self):
		sem1=Assessment.objects.get(title="Sem1")
		sem2=Assessment.objects.get(title="Sem2")
		self.assertEqual(sem1.display(), 'RESULTS ARE HERE')
		self.assertEqual(sem2.display(), 'RESULTS ARE HERE')