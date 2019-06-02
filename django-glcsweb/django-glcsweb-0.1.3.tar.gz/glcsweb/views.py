from django.shortcuts import get_object_or_404, render, redirect
from .forms import CredentialsForm, AssignmentsForm, CourseForm
import os
import django
import gitlab
from datetime import datetime
import pytz
from glcs import main
from .models import *


def index(request):
    credentials = Credentials.objects.all()
    cred_list = []
    for credential in credentials:
        cred_list.append(credential.username)
    context = {}
    if 'user' in request.session:
        context['username'] = request.session['user']
        credential = Credentials.objects.get(username=request.session['user'])
        context['current_credentials'] = credential
        instructors = credential.instructor_set.all()
        courses = []
        for instructor in instructors:
            courses.append(instructor.course)
        context['courses'] = courses
        assignments = []
        for course in courses:
            for assignment in course.assignment_set.all():
                assignments.append(assignment)
        context['assignments'] = assignments
    context['cred_list'] = cred_list
    return render(request, 'web/index.html', context)

def login(request, username):
    request.session['user'] = username
    return redirect("web:index")

def signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CredentialsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            gitlab_token = form.cleaned_data['gitlab_token']
            gitlab_server = form.cleaned_data['gitlab_server']
            Credentials.objects.create(username=username, email=email, gitlab_token=gitlab_token, gitlab_server=gitlab_server)
            return redirect('web:index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CredentialsForm()

    return render(request, 'web/signup.html', {'form': form})

def newcourse(request):
    credentials = Credentials.objects.all()
    cred_list = []
    for credential in credentials:
        cred_list.append(credential.username)
    context = {}
    if 'user' in request.session:
        context['username'] = request.session['user']
        credential = Credentials.objects.get(username=request.session['user'])
        context['current_credentials'] = credential
        instructors = credential.instructor_set.all()
        courses = []
        for instructor in instructors:
            courses.append(instructor.course)
        context['courses'] = courses
    context['cred_list'] = cred_list
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CourseForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            username = context['current_credentials'].username
            name = form.cleaned_data['name']
            semester = form.cleaned_data['semester']
            mp_id = form.cleaned_data['mp_id']
            roster = form.cleaned_data['roster'].split('\n')
            graders = form.cleaned_data['graders'].split('\n')
            for grader in graders:
                grader = grader.strip()
            ps = {}
            ps['student_access'] = int(form.cleaned_data['student_access'])
            ps['grader_access'] = int(form.cleaned_data['grader_access'])
            ps['project_visibility'] = form.cleaned_data['project_visibility']
            create_course(username, name, semester, mp_id, roster, graders, ps)
            return redirect('web:index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CourseForm()

    context['form'] = form
    return render(request, 'web/course.html', context)

def course(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        course = None

    context = {
        'course': course,
    }
    return render(request, 'web/course.html', context)


def tas(request, course_id):


    context = {
        'course_id': course_id,
    }
    return render(request, 'web/ta.html', context)


def ta(request, course_id, ta_id):
    context = {
        'course_id': course_id,
        'ta_id': ta_id,
    }
    return render(request, 'web/ta.html', context)


def students(request, course_id):
    context = {
        'course_id': course_id,
    }
    return render(request, 'web/student.html', context)


def student(request, course_id, student_id):
    context = {
        'course_id': course_id,
        'student_id': student_id,
    }
    return render(request, 'web/student.html', context)


def assignments(request, course_id):
    credentials = Credentials.objects.all()
    cred_list = []
    for credential in credentials:
        cred_list.append(credential.username)
    context = {}
    form = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AssignmentsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            tag = form.cleaned_data['tag']
            type = 0
            if form.cleaned_data['type']:
                type = 1
            due_date = form.cleaned_data['due_date']
            mimir_project_id = None
            if form.cleaned_data['mimir_project_id'] != "":
                mimir_project_id = form.cleaned_data['mimir_project_id']
            course = Course.objects.get(pk=course_id)
            course.assignment_set.create(tag=tag, type=type, due_date=due_date, mimir_project_id=mimir_project_id)
            return redirect('web:assignments', course_id)
    else:
        form = AssignmentsForm()
    context['form'] = form
    if 'user' in request.session:
        context['username'] = request.session['user']
        credential = Credentials.objects.get(username=request.session['user'])
        context['current_credentials'] = credential
        instructors = credential.instructor_set.all()
        courses = []
        for instructor in instructors:
            courses.append(instructor.course)
        context['courses'] = courses
        course = Course.objects.get(pk=course_id)
        context['course'] = course
        assignments = []
        for assignment in course.assignment_set.all():
            assignments.append(assignment)
        context['assignments'] = assignments
    context['cred_list'] = cred_list
    # if this is a POST request we need to process the form data
    return render(request, 'web/assignments.html', context)


def assignment(request, course_id, assignment_id):
    context = {
        'course_id': course_id,
        'assignment_id': assignment_id,
    }
    return render(request, 'web/assignment.html', context)


def create_course(username, name, semester, mp_id, roster, graders, ps):
    credentials = Credentials.objects.get(username=username)
    gl = main.GLCS(credentials.gitlab_server, credentials.gitlab_token)
    out = gl.courses.setup_course(name, semester, mp_id, roster, graders, ps)
    settings = None
    try:
        settings = ProjectSettings.objects.get(student_access=ps["student_access"], grader_access=ps["grader_access"], project_visibility=ps["project_visibility"])
    except ProjectSettings.DoesNotExist:
        settings = ProjectSettings.objects.create(student_access=ps["student_access"], grader_access=ps["grader_access"], project_visibility=ps["project_visibility"])
    course = Course.objects.create(name=name, course_group_id=out['course_group_id'], course_project_id=mp_id, semester=semester, project_settings=settings)
    course.instructor_set.create(status=1, position=0, credential=credentials)
    for student in out['students']:
        course.student_set.create(username=student.username, email=student.email, student_group_id=student.group_id, student_project_id=student.project_id, status=1)
