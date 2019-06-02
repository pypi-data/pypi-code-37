"""Submit-project-project class"""
import argparse
import sys
import subprocess
import os
from pathlib import Path

def pull_directory(directory, remote_name, git_url, path):
    """Pull a specific directory from the given respository."""
    saved = os.getcwd()
    remote_branch = remote_name + '/master'
    if not Path(directory).exists():
        os.mkdir(directory)
    os.chdir(directory)
    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'remote', 'add', remote_name, git_url])
    subprocess.call(['git', 'fetch', remote_name])
    subprocess.call(['git', 'checkout', remote_branch, '--', path])
    os.chdir(saved)
    return directory

directory = pull_directory("temp", "test-project", "https://gitlabt.cs.unh.edu:8443/test16/gtl005/test16.git", "a1/")
print("dir: " + directory)

parser = argparse.ArgumentParser(description = 'Save flag arguments')
parser.add_argument("-u", help="Saves teacher username", action="store", dest="username")
parser.add_argument("-p", help="Saves teacher password", action="store", dest="passwd")
parser.add_argument("-e", help="Saves student email", action="store", dest="email")
parser.add_argument("-d", help="Saves directory name", action="store", dest="directory", default=None)
parser.add_argument("-i", help="Saves project id", action="store", dest="project_id")

results = parser.parse_args()

def Submit_for_student(username, psswd, email, project_id, directory=None):
    if username is None:
        sys.exit("Error: Need a mimir email")
    if psswd is None:
        sys.exit("Error: Need a mimir password")
    if email is None:
        sys.exit("Error: Need a student email to submit on behalf of")
    if project_id is None:
        sys.exit("Error: Need a mimir project UUID")
    if directory is None:
        subprocess.call(["./Submit-student-project.sh", "-u", username, "-p", psswd, "-e", email, "-i", project_id])
    else:
        subprocess.call(["./Submit-student-project.sh", "-u", username, "-p", psswd, "-e", email, "-d", directory, "-i", project_id])

Submit_for_student(results.username, results.passwd, results.email, results.project_id, results.directory)
