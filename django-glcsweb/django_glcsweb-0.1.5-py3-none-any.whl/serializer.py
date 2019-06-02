from rest_framework import serializers
from .models import (
    Course,
    ProjectSettings,
    Credentials,
    Instructor,
    Student,
    Assignment
)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'id',
            'name',
            'course_group_id',
            'course_project_id',
            'semester',
            'project_settings'
        )


class ProjectSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSettings
        fields = (
            'id',
            'student_access',
            'grader_access',
            'project_visibility'
        )


class CredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credentials
        fields = (
            'id',
            'username',
            'email',
            'gitlab_oauth',
            'gitlab_server'
        )


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = (
            'id',
            'status',
            'position',
            'credential',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'id',
            'username',
            'student_group_id',
            'student_project_id',
            'status',
            'course_instance'
        )


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = (
            'id',
            'tag',
            'types',
            'due_date',
            'mimir_project_id',
            'course_instance'
        )
