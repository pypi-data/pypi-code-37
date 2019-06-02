import codecs
import os
import sys
import subprocess
import random
import shutil
import string
from git import Repo

from django_crud_generator.django_crud_generator import render_template_with_args_in_file

# from django_bootstrapper.conf import *
DJANGO_VERSION_KEY = "django_version"
TEMPLATE_SUBMODULE_NAME_KEY = "template_folder_name"
PROJECT_ROOT_KEY = "project_root"
PROJECT_NAME_KEY = "project_name"
USE_SUBMODULES_KEY = "submodules"
ADD_SCRIPTS_KEY = "scripts"
DOCKER_IMAGE_KEY = "docker_image"
USER_MANAGEMENT = "user_management"
VERBOSITY_KEY = 0

INVALID_OPTION_MESSAGE = "Invalid option"
VALIDATING_OPTIONS_MESSAGE = "Validating options"
OPTIONS_VALIDATED_MESSAGE = "Options validated"
INSTALLING_DJANGO_MESSAGE = "Installing django"
CREATING_DIRECTORY_MESSAGE = "Creating directory"
DIRECTORY_ALREADY_EXISTS_MESSAGE = "Directory already exists"
CREATING_DJANGO_PROJECT_MESSAGE = "Creating Django project"
DJANGO_PROJECT_CREATED_MESSAGE = "Django project created"
INITIALIZING_GIT_REPOSITORY_MESSAGE = "Initializing git repository {}"
CREATING_SUBMODULES_MESSAGE = "Creating submodules"
SUBMODULE_ADDED_MESSAGE = "{} submodule added"
DOWNLOAD_SUBMODULES_MESSAGE = "Downloading submodules"
SUBMODULE_DOWNLOADED_MESSAGE = "{} submodule downloaded"
CREATING_EXTRA_FILES = "Creating extra files"

# For file commons
BASE_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


class DjangoBootstrapper(object):

    OPTION_DICT = {
        DJANGO_VERSION_KEY: 2.2,
        TEMPLATE_SUBMODULE_NAME_KEY: "contraslash/base_template-django",
        PROJECT_ROOT_KEY: ".",
        PROJECT_NAME_KEY: "config",
        USE_SUBMODULES_KEY: "False",
        ADD_SCRIPTS_KEY: "False",
        DOCKER_IMAGE_KEY: "contraslash/alpine-django-deploy-common",
        USER_MANAGEMENT: "False"
    }

    SUBMODULES = [
        {
            "name": "base",
            "path": "base",
            "url": "https://github.com/contraslash/base-django"
        },
        {
            "name": "authentication",
            "path": "applications/authentication",
            "url": "https://github.com/contraslash/authentication-django"
        }
    ]

    SUBMODULE_TEMPLATE = {
        "name": "template",
        "path": "applications/base_template",
        "url": "https://github.com/{}"
    }

    SUBMODULE_USER_MANAGEMENT = {
        "name": "user_management",
        "path": "applications/user_management",
        "url": "https://github.com/contraslash/user_management-django"
    }

    SCRIPTS = [
        "create_bucket.sh",
        "create_database.sql"
    ]

    def __init__(self):
        self.repository = None

    def update_options(self):
        """
        Updates OPTION_DICT dictionary with data from user
        :return:
        """
        for key, value in self.OPTION_DICT.items():
            string_to_show = "{} [{}]: ".format(key, value) if value else "{}: ".format(key)

            readed_value = input(string_to_show)
            self.OPTION_DICT[key] = readed_value if readed_value else value

    def re_calculate_submodules(self):
        if self.OPTION_DICT.get(TEMPLATE_SUBMODULE_NAME_KEY, ""):
            self.SUBMODULE_TEMPLATE["url"] = self.SUBMODULE_TEMPLATE["url"].format(
                self.OPTION_DICT.get(TEMPLATE_SUBMODULE_NAME_KEY, "")
            )
            self.SUBMODULES.append(self.SUBMODULE_TEMPLATE)
        if self.OPTION_DICT.get(USER_MANAGEMENT, "") == "True":
            self.SUBMODULES.append(self.SUBMODULE_USER_MANAGEMENT)

    def valid_options(self):
        """
        Validates option selected by the user
        :return:
        """
        print(VALIDATING_OPTIONS_MESSAGE)
        self.OPTION_DICT[PROJECT_ROOT_KEY] = os.path.abspath(
            self.OPTION_DICT[PROJECT_ROOT_KEY]
        )
        return True

    @staticmethod
    def install_django(version):
        """
        Installs django with the version given
        :param version: int
        :return:
        """
        print(INSTALLING_DJANGO_MESSAGE)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'django~={}'.format(version)])

    @staticmethod
    def create_django_project(name, path):
        """
        Uses django management to create a project in the specified folder
        :param name: name of project
        :param path: path to create a project
        :return:
        """
        print(CREATING_DJANGO_PROJECT_MESSAGE)
        from django.core.management import execute_from_command_line
        # command.handle('project', name, path, verbosity=verbosity)
        execute_from_command_line(['django-admin', 'startproject', name, path])
        print(DJANGO_PROJECT_CREATED_MESSAGE)

    def initialize_git_repo(self, path, use_submodules=True):
        """
        Create a project structure initializing the path folder and creating all submodule structure
        If submodules is False,
        :param path:
        :param use_submodules:
        :return:
        """
        print(INITIALIZING_GIT_REPOSITORY_MESSAGE.format(path))
        self.repository = Repo.init(path)
        # Create application folder
        applications_folder = os.path.join(path, "applications")
        if not os.path.exists(applications_folder):
            os.makedirs(applications_folder)
        open(os.path.join(applications_folder, "__init__.py"), "w+")

        if use_submodules:
            print(CREATING_SUBMODULES_MESSAGE)
            for submodule in self.SUBMODULES:

                self.repository.create_submodule(
                    submodule["name"],
                    os.path.join(path, submodule["path"]),
                    submodule["url"],
                )
                print(SUBMODULE_ADDED_MESSAGE.format(submodule["name"]))
        else:
            print(DOWNLOAD_SUBMODULES_MESSAGE)
            for submodule in self.SUBMODULES:
                Repo.clone_from(
                    submodule["url"],
                    os.path.join(path, submodule["path"]),
                )
                shutil.rmtree(os.path.join(path, submodule["path"], ".git"))
                print(SUBMODULE_DOWNLOADED_MESSAGE.format(submodule["name"]))
        self.repository.git.add(A=True)
        self.repository.index.commit("Creating first file structure")

    def create_extra_files(self, project_root, project_name, template_repo):
        """
        This functions create the extra files README.md and a settings_prod to your project folder
        :param project_root:
        :param project_name:
        :param template_repo:
        :return:
        """
        print(CREATING_EXTRA_FILES)
        DjangoBootstrapper.create_file_with_template_in_folder(
            "README.md",
            project_root,
            BASE_TEMPLATES_DIR,
            **{
                "project_name": project_name,
                "template_repo": template_repo
            }
        )
        project_config_folder = os.path.join(
            project_root,
            project_name
        )
        files_in_project_config_folder = ["settings_prod.py"]
        templates_config_folder = os.path.join(
            BASE_TEMPLATES_DIR,
            "project_config"
        )
        for file_in_project_config_folder in files_in_project_config_folder:
            self.create_file_with_template_in_folder(
                file_in_project_config_folder,
                project_config_folder,
                templates_config_folder,
                **{
                    "project_name": project_name,
                    "project_prefix": project_name.upper()
                }
            )
        self.repository.git.add(A=True)
        self.repository.index.commit("Creating first file structure")

    # For File commons
    @staticmethod
    def create_file(path):
        """
        This function creates a file
        :param path:
        :return:
        """
        return codecs.open(
            path,
            'w+',
            encoding='UTF-8'
        )

    # For File commons
    @staticmethod
    def create_directory(path):
        """
        This function creates a directory
        :param path:
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(path)

    # For File commons
    @staticmethod
    def create_file_with_template_in_folder(file, path, templates_path, **kwargs):
        """
        This function creates a file from a template in a specified directory, using kwargs
        :param file:
        :param path:
        :param templates_path:
        :param kwargs:
        :return:
        """
        render_template_with_args_in_file(
            DjangoBootstrapper.create_file(
                os.path.join(
                    path,
                    file
                )
            ),
            os.path.join(templates_path, "{}.tmpl".format(file)),
            **kwargs
        )

    def create_scripts(self):
        scripts_folder = os.path.join(
            self.OPTION_DICT[PROJECT_ROOT_KEY],
            "scripts"
        )
        self.create_directory(
            scripts_folder
        )
        templates_scripts_folder = os.path.join(
            BASE_TEMPLATES_DIR,
            "scripts"
        )
        for script in self.SCRIPTS:
            self.create_file_with_template_in_folder(
                script,
                scripts_folder,
                templates_scripts_folder,
                **{
                    "project_name": self.OPTION_DICT[PROJECT_NAME_KEY],
                    "random_password": "".join(random.choices(string.ascii_letters + string.digits, k=16))
                }
            )

    def add_docker(self):
        docker_files = [
            ".dockerignore",
            "Dockerfile",
            "requirements.txt",
            "uwsgi.ini",

        ]
        templates_docker_folder = os.path.join(
            BASE_TEMPLATES_DIR,
            "docker_config"
        )
        for docker_file in docker_files:
            self.create_file_with_template_in_folder(
                docker_file,
                self.OPTION_DICT[PROJECT_ROOT_KEY],
                templates_docker_folder,
                **{
                    "project_name": self.OPTION_DICT[PROJECT_NAME_KEY],
                    "django_version": self.OPTION_DICT[DJANGO_VERSION_KEY],
                    "docker_base_image": self.OPTION_DICT[DOCKER_IMAGE_KEY]
                }
            )

    def execute(self):
        self.update_options()

        self.re_calculate_submodules()

        if not self.valid_options():
            print(INVALID_OPTION_MESSAGE)
            exit(1)
        else:
            print(OPTIONS_VALIDATED_MESSAGE)

        self.install_django(
            version=self.OPTION_DICT[DJANGO_VERSION_KEY]
        )
        self.create_directory(
            path=self.OPTION_DICT[PROJECT_ROOT_KEY]
        )
        self.create_django_project(
            name=self.OPTION_DICT[PROJECT_NAME_KEY],
            path=self.OPTION_DICT[PROJECT_ROOT_KEY]
        )
        self.initialize_git_repo(
            path=self.OPTION_DICT[PROJECT_ROOT_KEY],
            use_submodules=self.OPTION_DICT[USE_SUBMODULES_KEY] == "True"
        )
        self.create_extra_files(
            project_root=self.OPTION_DICT[PROJECT_ROOT_KEY],
            project_name=self.OPTION_DICT[PROJECT_NAME_KEY],
            template_repo=self.OPTION_DICT[TEMPLATE_SUBMODULE_NAME_KEY],
        )

        if self.OPTION_DICT[ADD_SCRIPTS_KEY] == "True":
            self.create_scripts()

        if self.OPTION_DICT[DOCKER_IMAGE_KEY] != "None":
            self.add_docker()


def execute_from_command_line():
    django_bootstrapper = DjangoBootstrapper()
    django_bootstrapper.execute()


if __name__ == '__main__':
    execute_from_command_line()
