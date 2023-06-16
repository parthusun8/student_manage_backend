from rest_framework import serializers
from .models import Departments, Sections, Students, Subjects, Marks

class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Departments
        fields = ['dept_no', 'dept_name']

class SectionSerializer(serializers.HyperlinkedModelSerializer):
    dept_no = serializers.PrimaryKeyRelatedField(queryset=Departments.objects.all())
    class Meta:
        model = Sections
        fields = ['id', 'section_name', 'dept_no']

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    section_id = serializers.PrimaryKeyRelatedField(queryset=Sections.objects.all())
    dept_no = serializers.PrimaryKeyRelatedField(queryset=Departments.objects.all())
    class Meta:
        model = Students
        fields = ['name', 'email', 'regdno', 'section_id', 'dept_no', 'current_semester']

class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    dept_no = serializers.PrimaryKeyRelatedField(queryset=Departments.objects.all())
    class Meta:
        model = Subjects
        fields = ["id", "subject_name", "subject_code", 'credits',"type", "semester_no", "dept_no"]

class MarksSerializer(serializers.HyperlinkedModelSerializer):
    regdno = serializers.PrimaryKeyRelatedField(queryset=Students.objects.all())
    subject_id = serializers.PrimaryKeyRelatedField(queryset=Subjects.objects.all())
    class Meta:
        model = Marks
        fields = ['marks', 'regdno', 'subject_id']