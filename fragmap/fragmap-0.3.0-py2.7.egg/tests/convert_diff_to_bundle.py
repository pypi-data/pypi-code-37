#!/usr/bin/env python

# Take 1 argument: filename
# Read file
# Create a subfolder with same name as file but with ".bundle.dir" added
# Go into the subfolder
# git init
# Split by lines starting with "commit "
# For each set of lines, create a commit by calling git-apply and then commit with message from first line starting with "    "
# git-bundle the subdirectory repo with ".bundle" added to filename

import argparse
import subprocess
import os
import shutil
import stat

def group_before_lines_starting_with(prefix, lines):
  groups = []
  cur_group = [[]]
  def add_to_cur(s):
    return cur_group[0].append(s)
  def flush_group():
    if len(cur_group[0]) > 0:
      groups.append(cur_group[0])
      cur_group[0] = []
  for line in lines:
    if line.startswith(prefix):
      flush_group()
    add_to_cur(line)
  flush_group()
  return groups
assert([['12'], ['hello', 'world'],['he', 'weather']]
       == group_before_lines_starting_with('he', ['12', 'hello', 'world', 'he', 'weather']))

DEFAULT_GIT_CONFIG_STRING=["-c", "user.name='Foo Bar'", "-c", "user.email='foo@example.com'"]
DEFAULT_GIT_ENV={'GIT_COMMITTER_NAME': 'Foo Bar',
                 'GIT_COMMITTER_EMAIL': 'foo@example.com',
                 'GIT_CONFIG_NOSYSTEM': '1'}

def git_apply(diff_lines):
  print "Calling git apply in", os.getcwd()
  p = subprocess.Popen(['git'] + DEFAULT_GIT_CONFIG_STRING + ['apply', '--cached', '-'], stdin=subprocess.PIPE, env=DEFAULT_GIT_ENV)
  print "Input:"
  text = '\n'.join(diff_lines)
  print text
  p.communicate(text)

def git_commit(message):
  print "Calling git commit in", os.getcwd()
  subprocess.check_call(['git'] + DEFAULT_GIT_CONFIG_STRING + ['commit', '-m', message], env=DEFAULT_GIT_ENV)

def git_init(path):
  print "Calling git init in", os.getcwd()
  subprocess.check_call(['git'] + DEFAULT_GIT_CONFIG_STRING + ['init'], cwd=path, env=DEFAULT_GIT_ENV)

def git_bundle(repo_path, bundle_filename):
  print "Calling git bundle in", os.getcwd(), "cwd:", repo_path
  subprocess.check_call(['git'] + DEFAULT_GIT_CONFIG_STRING + ['bundle', 'create', bundle_filename, '--all'], cwd=repo_path, env=DEFAULT_GIT_ENV)

def get_message(diff_lines):
  def is_message_line(line):
    return line.startswith('    ')
  message = filter(is_message_line, diff_lines)
  return message[0].rstrip().lstrip(' ')

def delete_readonly(action, name, exc):
  os.chmod(name, stat.S_IWRITE)
  os.remove(name)

def main():
  p = argparse.ArgumentParser()
  p.add_argument('diff_file', metavar='DIFF_FILE')
  args = p.parse_args()

  repo_path = args.diff_file + ".bundle.dir"
  bundle_filename = args.diff_file + ".bundle"

  with open(args.diff_file, 'rb') as f:
    diff_file_lines = [line.rstrip() for line in f]
  commit_diffs = group_before_lines_starting_with("commit ", diff_file_lines)

  os.mkdir(repo_path)
  git_init(repo_path)
  old_cwd=os.getcwd()
  os.chdir(repo_path)
  for commit_diff_lines in commit_diffs:
    git_apply(commit_diff_lines)
    git_commit(get_message(commit_diff_lines))
  os.chdir(old_cwd)
  git_bundle(repo_path, os.path.join(os.getcwd(), bundle_filename))
  shutil.rmtree(repo_path, onerror=delete_readonly)

if __name__ == '__main__':
  main()

# Conventions
# branch name == diff name
#   branch 001-add-line-to-file.diff
# no branch named 001-base => the branch is just 1 commit
# get_diff('001-add-line-to-file', 'repo-name')
#   Navigate to repo-name
#   If branch named 001-base exists:
#     Get diff 001-base..001-add-line-to-file
#   Else:
#     Get diff 001-add-line-to-file^..001-add-line-to-file


# Have diffs in text in unit test body
# Have diffs applied by git in dedicated repo in order
# * Have bundled repos with one or more sequenes of commits for respective test case
#  Create repos for each with remotes = bundle file
#  Have to push before testing
#  Assume each commit has unique message -> can list the commits in each case
#  Repo is called same as test
# Have bundled repos and each test case in own file

# Information in test cases
# Ease of modification
# Ease of addition
# Ease of version control
# Brevity of test case

# repo -> bundle -> repo
