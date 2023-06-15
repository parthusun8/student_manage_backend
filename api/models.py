from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Departments(models.Model):
    dept_name = models.CharField(max_length=100)
    dept_no = models.IntegerField(primary_key=True)

    def __str__(self) -> str:
        return str(self.dept_no) + " - " + self.dept_name

class Sections(models.Model):
    section_name = models.CharField(max_length=5)
    dept_no = models.ForeignKey(Departments, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.dept_no.dept_name) + " - " + self.section_name

class Students(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    regdno = models.AutoField(primary_key=True)
    section_id = models.ForeignKey(Sections, on_delete=models.CASCADE)
    dept_no = models.ForeignKey(Departments, on_delete=models.CASCADE)
    current_semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])

    def __str__(self) -> str:
        return self.name + " - " +str(self.regdno)

class Subjects(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=100)
    semester_no = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    type = models.CharField(max_length=100, choices=[('theory', 'theory'), ('lab', 'lab')])
    dept_no = models.ForeignKey(Departments, on_delete=models.CASCADE)
    credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    def __str__(self) -> str:
        return f"Semester {self.semester_no} " + self.subject_code +" - " + self.subject_name + " - " + ('T' if self.type=='theory' else 'L')

class Marks(models.Model):
    marks = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    regdno = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
