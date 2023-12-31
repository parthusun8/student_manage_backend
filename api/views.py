from django.shortcuts import render
from rest_framework import viewsets
from .models import Departments, Sections, Students, Subjects, Marks
from .serializers import StudentSerializer, SubjectSerializer, MarksSerializer, DepartmentSerializer, SectionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
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
            # print(count_students)
            # print(serializer.data)
            for i in range(len(serializer.data)):
                serializer.data[i]['count_students'] = Students.objects.filter(section_id=serializer.data[i]["id"]).count()
            return Response(serializer.data)
        except Exception as e:
            print(e)

    @action(detail=True, methods=['get'])
    def subjects(self, request, pk=None):
        try:
            subjects = Subjects.objects.filter(dept_no=pk)
            serializer = SubjectSerializer(subjects, many=True, context={'request': request})
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



def get_grade_from_marks(marks):
    if marks > 90:
        return 'O', 10
    elif marks > 80:
        return 'A+', 9
    elif marks > 70:
        return 'A', 8
    elif marks > 60:
        return 'B', 7
    elif marks > 50:
        return 'C', 6
    elif marks > 40:
        return 'D', 5
    else:
        return 'E', 4

@require_GET
def get_student_marks(request, student_id):
    try:
        student = Students.objects.get(regdno=student_id)
        data = []
        cgpa = 0
        for i in range(1, student.current_semester + 1):
            subjects = Subjects.objects.filter(dept_no=student.dept_no, semester_no=i)
            marks = Marks.objects.filter(regdno=student_id, subject_id__in=subjects)
            theory = []
            lab = []
            total = 0
            total_credits = 0
            for mark in marks:
                grade, score = get_grade_from_marks(mark.marks)
                if mark.subject_id.type == 'theory':
                    theory.append({
                        'subject_name': mark.subject_id.subject_name,
                        'marks': mark.marks,
                        'subject_code': mark.subject_id.subject_code,
                        'grade' : grade
                    })
                else:
                    lab.append({
                        'subject_name': mark.subject_id.subject_name,
                        'marks': mark.marks,
                        'subject_code': mark.subject_id.subject_code,
                        'grade' : grade
                    })
                total_credits += mark.subject_id.credits
                total += (score * mark.subject_id.credits)
                print(total, total_credits)
                gpa = total/total_credits
            data.append({
                'semester': i,
                'subjects': {
                    "theory": theory,
                    "lab": lab
                },
                "sgpa": round(gpa,2),
                "grade" : get_grade_from_marks(gpa*10)[0]
            })
            cgpa += gpa
        cgpa = cgpa/student.current_semester
        data.reverse()
        return JsonResponse({'Marks': data, "cgpa": cgpa})
    except Students.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    



def get_data_for_a_student(regdno):
    student = Students.objects.get(regdno=regdno)
    data = []
    cgpa = 0
    for i in range(1, student.current_semester + 1):
        subjects = Subjects.objects.filter(dept_no=student.dept_no, semester_no=i)
        marks = Marks.objects.filter(regdno=regdno, subject_id__in=subjects)
        total = 0
        total_credits = 0
        for mark in marks:
            _, score = get_grade_from_marks(mark.marks)
            total_credits += mark.subject_id.credits
            total += (score * mark.subject_id.credits)
            # print(total, total_credits)
            gpa = total/total_credits
        data.append({
            'semester': i,
            "sgpa": round(gpa,2),
            "grade" : get_grade_from_marks(gpa*10)[0]
        })
        cgpa += gpa
    cgpa = cgpa/student.current_semester
    data.reverse()
    return {
        'name' : student.name,
        'regdno' : student.regdno,
        'dept_no' : student.dept_no.dept_name,
        'section_id' : student.section_id.section_name,
        'current_semester' : student.current_semester,
        'data' : data,
        'cgpa' : round(cgpa,2)
    }


@require_GET
def compare_two_students(request, student_id1, student_id2):
    try:
        stud1 = get_data_for_a_student(student_id1)
        stud2 = get_data_for_a_student(student_id2)
        compare = [
            stud1,
            stud2
        ]
        return JsonResponse({'data' : compare})
    except Students.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)


@csrf_exempt
@require_POST
@api_view(['POST'])
def upload_csv(request):
    try:
        print(request.FILES)
        file = request.FILES['file']
        if not file.name.endswith('.csv'):
            return Response({"error": "File is not csv"}, status=400)
        file_data = file.readlines()
        print(file_data[0])
        dept_id, section_id = [int(i) for i in file_data[0].decode("utf-8").split('\r\n')[0].split(',')[:2]]
        print(dept_id, section_id)
        students = []
        student_details = []
        for line in file_data[1:]:
            fields = line.decode("utf-8").split('\r\n')[0].split(',')
            print(fields)
            curr = Students(
                regdno=int(fields[0]),
                name=fields[1],
                email=fields[2],
                dept_no=Departments.objects.get(dept_no=dept_id),
                section_id=Sections.objects.get(id=section_id),
                current_semester=int(fields[3])
            )
            students.append(curr)
            curr.save()
            student_details.append({
                'regdno': int(fields[0]),
                'name': fields[1],
                'email': fields[2],
                'dept_no': dept_id,
                'section_id': section_id,
                'current_semester': int(fields[3])
            })
        return Response({"details" : student_details}, status=200)
    except Exception as e:
        print(e)
        return Response({"error": "Something went wrong"}, status=500)