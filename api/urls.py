from django.urls import path, include
from .views import DepartmentViewSet,SectionViewSet, StudentViewSet, SubjectViewSet, MarksViewSet, get_student_marks
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'marks', MarksViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'sections', SectionViewSet)

# print(router.urls)
urlpatterns = [
    path('', include(router.urls)),
    path('allSubjects/<int:student_id>/', get_student_marks)
]
