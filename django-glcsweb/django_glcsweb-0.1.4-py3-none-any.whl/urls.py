from django.urls import path

from . import views

app_name = "glcsweb"
urlpatterns = [
    path('', views.index, name='index'),
    path('login/<str:username>/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('course/new/', views.newcourse, name="newcourse"),
    path('course/<int:course_id>/', views.course, name='courseoverview'),
    path('course/<int:course_id>/tas/', views.tas, name='tas'),
    path('course/<int:course_id>/ta/<int:ta_id>/', views.ta, name='ta'),
    path('course/<int:course_id>/students/', views.students, name='students'),
    path('course/<int:course_id>/student/<int:student_id>/', views.student, name='student'),
    path('course/<int:course_id>/assignments/', views.assignments, name='assignments'),
    path('course/<int:course_id>/assignment/<int:assignment_id>', views.assignment, name='assignment'),
]
