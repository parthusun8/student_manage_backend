from django.shortcuts import render
from rest_framework import viewsets
from .models import Departments, Sections, Students, Subjects, Marks
from .serializers import StudentSerializer, SubjectSerializer, MarksSerializer, DepartmentSerializer, SectionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.http import require_GET
from django.http import JsonResponse

class DepartmentViewSet(viewsets.ModelViewSet):
    try:
        queryset = Departments.objects.all()
        serializer_class = DepartmentSerializer
    except Exception as e:
        print(e)

    @action(detail=True, methods=['get'])
    def sections(self, request, pk=None):
        print("Here")
        try:
            sections = Sections.objects.filter(dept_no=pk)
            serializer = SectionSerializer(sections, many=True, context={'request': request})
            count_students = Students.objects.filter(section_id__in=sections).count()
            print(count_students)
            print(serializer.data)
            for i in range(len(serializer.data)):
                serializer.data[i]['count_students'] = Students.objects.filter(section_id=serializer.data[i]["id"]).count()
            return Response(serializer.data)
        except Exception as e:
            print(e)

class SectionViewSet(viewsets.ModelViewSet):
    try:
        queryset = Sections.objects.all()
        serializer_class = SectionSerializer
    except Exception as e:
        print(e)

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        try:
            students = Students.objects.filter(section_id=pk)
            serializer = StudentSerializer(students, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            print(e)

class StudentViewSet(viewsets.ModelViewSet):
    try:
        queryset = Students.objects.all()
        serializer_class = StudentSerializer
    except Exception as e:
        print(e)

    @action(detail=True, methods=['get'])
    def subjects(self, request, pk=None):
        print("get subjects of particular student")
        try:
            subjects = Marks.objects.filter(regdno=pk)
            subjects = MarksSerializer(subjects, many=True, context={'request': request})
            return Response(subjects.data)
        except Exception as e:
            print(e)
            return Response({"error": "No such student"})
        

class SubjectViewSet(viewsets.ModelViewSet):
    try:
        queryset = Subjects.objects.all()
        serializer_class = SubjectSerializer
    except Exception as e:
        print(e)

class MarksViewSet(viewsets.ModelViewSet):
    try:
        queryset = Marks.objects.all()
        serializer_class = MarksSerializer
    except Exception as e:
        print(e)


@require_GET
def get_student_marks(request, student_id):
    try:
        student = Students.objects.get(regdno=student_id)
        
        
        # Prepare the response data
        data = []
        for i in range(1, student.current_semester + 1):
            subjects = Subjects.objects.filter(dept_no=student.dept_no, semester_no=i)
            print(subjects)
            marks = Marks.objects.filter(regdno=student_id, subject_id__in=subjects)
            theory = []
            lab = []
            for mark in marks:
                if mark.subject_id.type == 'theory':
                    theory.append({
                        'subject_name': mark.subject_id.subject_name,
                        'marks': mark.marks,
                        'subject_code': mark.subject_id.subject_code
                    })
                else:
                    lab.append({
                        'subject_name': mark.subject_id.subject_name,
                        'marks': mark.marks,
                        'subject_code': mark.subject_id.subject_code
                    })
            data.append({
                'semester': i,
                'subjects': {
                    "theory": theory,
                    "lab": lab
                }
            })
        
        return JsonResponse({'Marks': data})
    except Students.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
