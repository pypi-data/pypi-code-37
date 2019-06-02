from django.db import models


class ProjectSettings(models.Model):
    ACCESS_CHOICES = (
        (30, 'Maintainer access'),
        (40, 'Developer access'),
    )
    VISIBILITY_CHOICES = (
        ('private', 'private'),
        ('internal', 'internal'),
        ('public', 'public'),
    )
    student_access = models.IntegerField("Student access level",
                                         choices=ACCESS_CHOICES)
    grader_access = models.IntegerField("Grader/TA access level",
                                        choices=ACCESS_CHOICES)
    project_visibility = models.CharField("Visibility of the project",
                                          max_length=15,
                                          choices=VISIBILITY_CHOICES)

    def field_count(self):
        return 3

    def __str__(self):
        pk = str(self.pk)
        sa = str(self.student_access)
        ga = str(self.grader_access)
        pv = self.project_visibility[0:3]
        return pk + ": " + sa + " " + ga + " " + pv

    class Meta:
        unique_together = (
            'student_access',
            'grader_access',
            'project_visibility',
        )
        verbose_name = 'Project Setting'
        verbose_name_plural = 'Project Settings'


class Credentials(models.Model):
    username = models.CharField("Instructors username", max_length=30, unique=True)
    email = models.CharField("Instructor email", max_length=50, unique=True)
    gitlab_token = models.CharField("OAuth token from GitLab", max_length=100)
    gitlab_server = models.CharField("GitLab server URL", max_length=100)

    def __str__(self):
        return self.email

    def field_count(self):
        return 3

    class Meta:
        verbose_name = 'Credential'
        verbose_name_plural = 'Credentials'


class Course(models.Model):
    name = models.CharField("Course name", max_length=10)
    course_group_id = models.IntegerField("GitLab course group id")
    course_project_id = models.IntegerField("GitLab master project id")
    semester = models.CharField("Semester course is held", max_length=7)
    project_settings = models.ForeignKey(ProjectSettings,
                                         on_delete=models.CASCADE)

    def field_count(self):
        return 5

    def __str__(self):
        return self.name + "." + self.semester


class Instructor(models.Model):
    STATUS_CHOICES = (
        (0, "inactive"),
        (1, "active"),
    )
    POSITION_CHOICES = (
        (0, "Professor"),
        (1, "TA"),
    )
    status = models.IntegerField("Instructor status", choices=STATUS_CHOICES)
    position = models.IntegerField("Instructor type/position", choices=POSITION_CHOICES)
    credential = models.ForeignKey(Credentials, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def field_count(self):
        return 4

    def __str__(self):
        return self.credential.email


class Student(models.Model):
    STATUS_CHOICES = (
        (0, "inactive"),
        (1, "active"),
    )
    username = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    student_group_id = models.IntegerField("The students gitlab group id")
    student_project_id = models.IntegerField("The students gitlab project id")
    status = models.IntegerField("The students status", choices=STATUS_CHOICES)
    course_instance = models.ForeignKey(Course, on_delete=models.CASCADE)

    def field_count(self):
        return 5

    def __str__(self):
        return self.username


class Assignment(models.Model):
    TYPE_CHOICES = (
        (0, 'Assignment'),
        (1, 'Lab'),
    )
    tag = models.CharField("The assignment name/tag", max_length=10)
    type = models.IntegerField("Assignment type", choices=TYPE_CHOICES, default=0)
    due_date = models.DateTimeField()
    mimir_project_id = models.CharField("Project UUID within Mimir", max_length=45, null=True)
    course_instance = models.ForeignKey(Course, on_delete=models.CASCADE)

    def field_count(self):
        return 5

    def __str__(self):
        return self.tag
