# -*- coding: utf-8 -*-
"""CourseManager and Course classes."""
import os
from pathlib import Path
import gitlab
import jinja2
from glcs.group import GroupManager, Group
from glcs.student import Student
from glcs import group
from glcs import constants as c


def parse_roster(roster, email=False):
    """Extract desired information from a string representation of a roster
    file.

    Args:
        roster: string representation of a roster file
        email: whether email should be parsed as well as username

    Returns:
        A list of student usernames, or a list of dictionaries containing
        student emails and usernames if email param is specified.
    """
    if not email:
        students = []
        for line in roster:
            if not line.strip():
                continue
            line = line.strip()
            line = line.split("|")
            students.append(line[0])
        return students
    else:
        students = []
        for line in roster:
            if not line.strip():
                continue
            student = {}
            line = line.strip()
            line = line.split("|")
            print(line)
            student['username'] = line[0]
            student['email'] = line[16]
            students.append(student)
        return students


class CourseManager:
    """Simplifies the handling of courses.

    Supplies a set of common functions for manipulating courses.

    Attributes:
        gitlab: A gitlab.Gitlab object from the python-gitlab package
        instructor: A gitlab.v4.objects.CurrentUser object which represents
            the instructors login to GitLab
    """

    def __init__(self, gl):
        """Set up Gitlab and gather instructor information.

        Args:
            gl (gitlab.Gitlab): The handle used to access the gitlab API.
        """

        self.gitlab = gl

        self.gitlab.auth()

        self.instructor = self.gitlab.user

    def setup_course(self, name, semester, mp_id, roster, graders, ps):
        """Create a course from a set of course options and a class rosterfile.

        Runs verify_course after course creation.

        Args:
            name (str): The course name (and section if applicable).
            semester (str): The semester that course is being held.
            mp_id (int): The gitlab project id of the master project for the
                course.
            roster (str): The string representation of the roster file to
                create the course using.
            graders (list of str): A list of graders to add to
                the students projects and subgroups.

        Returns:
            A dictionary representation of the course, created using
            Course.to_dict().
        """

        course = Course(self.gitlab, name, semester, mp_id)
        course.setup(roster, graders, ps)
        self.verify_course(name, mp_id, roster, graders, ps)
        return course.to_dict()

    def verify_course(self, name, mp_id, roster, graders, ps):
        """[summary]
        
        Args:
            name ([type]): [description]
            mp_id ([type]): [description]
            roster ([type]): [description]
            graders ([type]): [description]
            ps ([type]): [description]
        """
        gl = self.gitlab
        className = name
        project_id = mp_id
        masterproj = gl.projects.get(project_id)
        project_name = masterproj.name
        gmanager = group.GroupManager(gl)
        grp = gmanager.get(name=className)
        subgroups = grp.list_subgroups()
        self.check_student_settings(
            className, roster, subgroups, gl, ps, graders, project_name)

    # Goes through each student and checks their settings
    def check_student_settings(self, courseName, rost, subgr, git, ps, graders, projName):
        output_list = []
        incorrect_student_settings = 0
        correct_student_settings = 0
        errorLog = []
        students = parse_roster(rost)
        subgroup = subgr
        for student in students:
            output_dictionary = {
                "Username": "",
                "Project": "",
                "Student_access": "",
                "Visibility": "",
                "Graders": {},
                "incorrect_settings": "",
                "correct_settings": ""
            }
            name = student
            output_dictionary["Username"] = name
            print("Check: " + name)
            output_dictionary, errorLog, isMember = self.check_group_settings(courseName, name, git, output_dictionary, students, subgroup,
                                                                              errorLog, incorrect_student_settings, correct_student_settings, projName, ps, graders)
            if not isMember:
                notMember = name + " is in the roster file but doesn't have an account in gitlab"
                errorLog.append(notMember)

            for grader in graders:
                if grader not in output_dictionary["Graders"]:
                    output_dictionary["incorrect_settings"] = True

            if output_dictionary["incorrect_settings"] == "":
                output_dictionary["correct_settings"] = True
                output_dictionary["incorrect_settings"] = False
                correct_student_settings = correct_student_settings + 1
            else:
                output_dictionary["correct_settings"] = False
                incorrect_student_settings = incorrect_student_settings + 1
            print("name: " + name)
            output_list.append(output_dictionary)
        print(str(output_list))
        self.render_html_output(output_list, incorrect_student_settings, correct_student_settings,
                                projName, errorLog, ps, courseName, graders)

    def check_group_settings(self, courseName, name, git, outdict, stud, subgr, error, incorrect,
                             correct, projName, ps, graders):
        incorrect_student_settings = incorrect
        correct_student_settings = correct
        output_dictionary = outdict
        expected_visibility = ps['project_visibility']
        errorLog = error
        subgroups = subgr
        project_name = projName
        gl = git
        isMember = False
        for sub in subgroups:
            if sub.name not in stud:
                errorMes = "has an account in gitlab but isn't in the roster"
                if (sub.name + errorMes) not in errorLog:
                    incorrect_student_settings += 1
                    errorLog.append(sub.name + errorMes)
            if sub.name == name:
                isMember = True
                real_group = gl.groups.get(sub.id)
                visibility = sub.visibility
                project = real_group.search('projects', project_name)
                path = project[0]['path_with_namespace']
                sub_mem = real_group.members.list()
                output_dictionary = self.check_sub_member_settings(
                    name, sub_mem, output_dictionary, ps, graders, errorLog)
                if (len(output_dictionary["Graders"]) == 0 and len(graders) > 0):
                    output_dictionary["Graders"] = "None"
                    output_dictionary["incorrect_settings"] = True

                # Check if user has visibility set to private
                if visibility == expected_visibility:
                    output_dictionary["Visibility"] = str(visibility)
                else:
                    output_dictionary["Visibility"] = str(visibility)
                    output_dictionary["incorrect_settings"] = True

                # Check if user has projects in their subgroup
                expected_path = courseName + "/" + name + "/" + project_name
                if path.lower() == expected_path.lower():
                    output_dictionary["Project"] = project_name
                else:
                    output_dictionary["Project"] = "NOT " + project_name
                    output_dictionary["incorrect_settings"] = True
        #print("Check dict1: " + str(output_dictionary))
        return output_dictionary, errorLog, isMember

    def check_sub_member_settings(self, name, sub, dict, ps, graders, error):
        errorLog = error
        access_level_conv = {
            10: "GUEST_ACCESS",
            20: "REPORTER_ACCESS",
            30: "DEVELOPER_ACCESS",
            40: "MAINTAINER_ACCESS",
            50: "OWNER_ACCESS"
        }
        sub_mem = sub
        output_dictionary = dict
        print("sub mem: " + str(sub_mem))
        for mem in sub_mem:
            print("mem: " + str(mem))
            if mem.username == name:
                sub_access = mem.access_level
                if sub_access == ps['student_access']:
                    output_dictionary["Student_access"] = str(
                        access_level_conv[sub_access])
                else:
                    output_dictionary["Student_access"] = "NOT " + \
                        str(access_level_conv[ps["student_access"]])
                    output_dictionary["incorrect_settings"] = True
            else:
                for grader in graders:
                    print("grader name: " + mem.username)
                    if (mem.username not in graders and mem.access_level == ps['grader_access']):
                        if (name + " has unnecessary grader, " + mem.username not in errorLog):
                            errorLog.append(
                                name + " has unnecessary grader, " + mem.username)
                    if grader == mem.username:
                        grader_name = mem.username
                        print("grader: " + grader_name)
                        grader_sub_access = mem.access_level

                        # Check access level of grader
                        if grader_sub_access == ps['grader_access']:
                            output_dictionary["Graders"][grader_name] = str(
                                access_level_conv[grader_sub_access])
                        else:
                            output_dictionary["Graders"][grader_name] = str(
                                access_level_conv[grader_sub_access])
                            output_dictionary["incorrect_settings"] = True
                    else:
                        print("Not a grader: " + str(mem.username))
                        print("Expected grader: " + str(graders))
        return output_dictionary

    def render_html_output(self, output, incorrect, correct, projName, error, ps,
                           courseName, graders):
        access_level_conv = {
            10: "GUEST_ACCESS",
            20: "REPORTER_ACCESS",
            30: "DEVELOPER_ACCESS",
            40: "MAINTAINER_ACCESS",
            50: "OWNER_ACCESS"
        }
        render_vars = {
            "course": courseName, "users": output,
            "incorrect_settings": incorrect,
            "correct_settings": correct, "expected_project": projName,
            "expected_student_access": access_level_conv[ps['student_access']],
            "expected_grader_access": access_level_conv[ps['grader_access']],
            "errorLog": error, "grader_names": graders
        }

        script_path = os.path.dirname(os.path.realpath(__file__))
        home_path = str(Path.home())
        template_file_location = os.path.join(script_path, 'templates')
        rendered_file_path = os.path.join(
            home_path, courseName+"-setup-results.html")
        environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_file_location))
        output_text = environment.get_template(
            'verify_output.html').render(render_vars)
        with open(rendered_file_path, "w+") as result_file:
            result_file.write(output_text)


class Course:
    """Handles Course-wide functions and data."""

    def __init__(self, gl, name, semester, master_proj_id):
        """Read the supplied options file and gets a list of students."""
        self.gmanager = GroupManager(gl)
        self.students = list()
        self.graders = list()
        self.course_name = name
        self.semester = semester
        self.group_name = str(name) + "." + str(semester)
        self.group = self.gmanager.get(name=self.group_name)
        self.project_settings = dict()
        self.master_proj_id = master_proj_id
        self.master_project = gl.projects.get(master_proj_id)
        self.gitlab = gl
        self.instructor = self.gitlab.user

    def setup(self, roster, grds, project_settings):
        """Set up this course."""
        students = parse_roster(roster, email=True)
        self.graders = grds
        gl_graders = []
        for grader in self.graders:
            grader = grader.strip()
            gl_graders.append(self.gitlab.users.list(username=grader)[0])
        self.graders = gl_graders
        self.project_settings = project_settings
        self.group = self.gmanager.create(name=self.group_name)
        if self.group is None:
            print("Group with name " + self.group_name + " already exists")
            return

        self.students = self.add_students(students)

        self.add_graders(gl_graders)

    def to_dict(self):
        course_dict = {
            'name': self.course_name,
            'semester': self.semester,
            'instructor': self.instructor,
            'course_group_id': self.group.id,
            'course_project_id': self.master_proj_id,
            'project_settings': self.project_settings,
            'students': self.students
        }
        return course_dict

    def add_students(self, students):
        """Add the list of students to the course."""
        student_list = []
        for student in students:
            student_list.append(self.add_student(student))
        return student_list

    def add_student(self, student):
        """Add a single student to the course."""
        settings = self.project_settings
        grp = self.group

        user = self.gitlab.users.list(username=student['username'])[0]
        username = user.username
        email = student['email']
        user_group = self.gmanager.create(name=username, parent=grp)
        if user_group is None:
            print("Group with name " + grp.name + "/" + username +
                  " already exists")
        student_proj = self.fork_master_proj(user, user_group)
        user_group.add_member(user, settings['student_access'])
        return Student(username, email, user_group.id, student_proj.id, 1)

    def fork_master_proj(self, student, user_group):
        """Fork the master project into the student group."""
        gl = self.gitlab
        master_proj = self.master_project
        grp = self.group
        namespace = grp.name + '/' + student.username
        fork_name = str(grp.name +
                        '/' + user_group.name +
                        '/' + master_proj.name)
        master_proj.forks.create({'namespace': namespace})
        student_proj = gl.projects.get(fork_name)
        student_proj.visibility = self.project_settings['project_visibility']
        self.add_assignment_hook(student_proj)
        student_proj.save()
        return student_proj

    def add_to_student_project(self, user_proj, user, access_level):
        """Add a user to a students project with the given access_level."""
        if not user_proj.members.list(query=user.username):
            user_proj.members.create({'user_id': user.id,
                                      'access_level': access_level})
        else:
            member = user_proj.members.get(user.id)
            member.access_level = access_level
            member.save()

    def add_graders(self, graders):
        """Add the list of graders to the course."""
        settings = self.project_settings
        for grader in graders:
            self.group.add_member(grader, settings['grader_access'])

    def assignment_hook_exists(self, student_proj):
        """Return whether or not a hook already exists."""
        hooks = student_proj.hooks.list()
        for hook in hooks:
            url = hook.url
            test_url = url[0:url.rindex('/')+1]
            if (test_url == c.HOOK_BASE_ASSIGNMENT_URL and
                    hook.push_events == 1 and
                    hook.tag_push_events == 1):
                return True

        return False

    def add_assignment_hook(self, student_proj):
        """Add an assignment hook to the project."""
        hook_attrs = {
            'url': c.HOOK_BASE_ASSIGNMENT_URL+str(self.group.id),
            'push_events': 1,
            'tag_push_events': 1
        }
        print("adding hook:")
        print(hook_attrs)
        if not self.assignment_hook_exists(student_proj):
            student_proj.hooks.create(hook_attrs)
