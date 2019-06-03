#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jira import JIRA, JIRAError
from rbtools.api.client import RBClient
import subprocess
import re
import os
import platform
from sourcefile import SourceFile
from hbt import check_commit_message_conventions


SUCCESS = ''


class Action(object):
    subject_re = r'^\s*(feat|fix|docs|style|refactor|chore)?\s*\((.*)\)\s*[:|：]\s*(.+)\n'
    new_line_re = r'\n'
    body_re = r'((?:.+\n)+)'
    affect_re = r'^([测试影响|影响].*)'
    commit_re = subject_re + new_line_re + body_re + new_line_re + affect_re

    rename_re = r'^\s*R\d+\s+.+[\.java|\.xml]\s+(.+(\.java|\.xml))\s*$'
    update_re = r'^\s*[M|A]\s+(.+(\.java|\.xml))\s*$'

    GROUP_INDEX_FILE_NAME = 1

    STATUS_SUBMITTED = 'submitted'

    def __init__(self, config, ctx, commit_message=''):
        self.config = config
        self.context = ctx
        self.debug = ctx.params['debug'] if ctx else False
        self.commit_message = commit_message or subprocess.check_output('git log --format=%B -n 1', shell=True).strip()

    def get_issue_id(self):
        return re.compile(self.subject_re).match(self.commit_message).group(2)

    def get_review_request_by_id(self, request_id):
        client = RBClient(self.config.reviewboard_url)
        return client.get_root().get_review_request(review_request_id=request_id)

    def get_review_url(self, lines=None):
        if not lines:
            lines = self.commit_message.split('\n')
        review_request_pattern = re.compile(r'^\s*%s/r/(\d+)/\s*$' % self.config.reviewboard_url)
        for line in lines:
            result = review_request_pattern.match(line)
            if result:
                return line, result.group(1)
        else:
            print(u'[WARN]: 没有解析到reviewboard url')
            return None, None

    def get_committed(self):
        commit_log = subprocess.check_output('git log --name-status --pretty=format:"" -n 1', shell=True)
        return [SourceFile.create(os.path.dirname(f), os.path.basename(f)) for f in
                self.get_commit_file_list(commit_log.split('\n'))]

    def get_commit_file_list(self, lines):
        files = list()
        rename_pattern = re.compile(self.rename_re)
        update_pattern = re.compile(self.update_re)
        for line in lines:
            result = rename_pattern.match(line)
            if result:
                files.append(result.group(self.GROUP_INDEX_FILE_NAME))
                continue

            result = update_pattern.match(line)
            if result:
                files.append(result.group(self.GROUP_INDEX_FILE_NAME))

        return files

    def amend_message(self):
        return SUCCESS if subprocess.call('git commit -a --amend --no-edit', shell=True) == 0 else \
               u'更新commit message失败'

    def printDebugLog(self, message):
        if self.debug:
            print message


class RbtPostArgsCheckAction(Action):
    branch_param_re = r'--branch.*'
    def do(self):
        if not self.config.branch_check:
            return SUCCESS
        self.printDebugLog('[hbt2] 命令参数合法性检查中...')
        branch_param_pattern = re.compile(self.branch_param_re)
        for arg in self.context.params['rbt_args']:
            if arg == '-r' or arg == '-u':
                return SUCCESS
            elif branch_param_pattern.match(arg):
                return SUCCESS
        return u'WARNING: 必须指定远程branch名称，请使用--branch来指定'


class WorkspaceCleanAction(Action):
    def do(self):
        self.printDebugLog('[hbt2] Workspace状态检查中...')
        if self.config.clean_check and \
                '' != subprocess.check_output('git status --porcelain --untracked-files=no', shell=True):
            return u'WARNING: 有未commit的文件。请commit后再发送review request'
        return SUCCESS


class CommitCheckAction(Action):
    def do(self):
        self.printDebugLog('[hbt2] Commit Message合法性检查中...')
        if check_commit_message_conventions(self.commit_message.split('\n')) == None:
            return u'WARNING: commit message格式不合格，请按提示修正。'
        return SUCCESS



class LandCheckAction(Action):
    def do(self):
        review_url, request_id = self.get_review_url()
        if not request_id:
            return u'未能查询到review request id'

        print(u'开始检查review request是否能够提交： ' + request_id)
        review_request = self.get_review_request_by_id(request_id)

        if not review_request.approved:
            print(review_request.approval_failure)
            return u'reviewboard检查失败'

        if not self.exist_remote_branch():
            return u'不存在的远程分支。请检查分支名。'

        return SUCCESS

    def exist_remote_branch(self):
        remote_name = 'remotes/origin/{}'.format(self.context.params['branch'])

        for line in subprocess.check_output('git branch -a', shell=True).split('\n'):
            if line.strip() == remote_name:
                return True
        else:
            return False


class PushAction(Action):
    def do(self):
        return SUCCESS if subprocess.call('git push origin HEAD:' + self.context.params['branch'], shell=True) == 0 \
                       else u'push失败'


class JiraUpdateAction(Action):
    def do(self):
        authed_jira = JIRA(server=self.config.jira_url, basic_auth=(self.config.jira_user, self.config.jira_password))
        issue = authed_jira.issue(self.get_issue_id())
        authed_jira.add_comment(issue, self.commit_message)

        # '4' 代表状态是 开发中
        try:
            authed_jira.transition_issue(issue, transition='4')
        except JIRAError:
            # 当jira状态已经为“开发中”时，这里transition会抛异常。ignore it
            pass
        return SUCCESS


class CloseReviewboardAction(Action):
    def do(self):
        commit_id = subprocess.check_output('git log --format="%H" -n 1', shell=True)
        description = 'hbt closed: {}'.format(commit_id)

        _, request_id = self.get_review_url()
        if not request_id:
            return u'未能查询到review request id'

        review_request = self.get_review_request_by_id(request_id)
        if review_request.status == self.STATUS_SUBMITTED:
            return u'Review request {} is already submitted.'.format(request_id)

        review_request.update(status=self.STATUS_SUBMITTED, description=description)
        return SUCCESS


class CopyrightUpdateAction(Action):
    def do(self):
        self.printDebugLog('[hbt2] Copyright自动处理中...')
        for f in self.get_committed():
            f.add_copyright()
        self.amend_message()
        return SUCCESS


class StyleCheckAction(Action):
    CYGWIN_SYSTEM_PREFIX = 'CYGWIN'
    CHECKSTYLE_JAR_FILE_NAME = 'checkstyle-all.jar'
    CHECKSTYLE_CONFIG_FILE_NAME = 'checkstyle-config.xml'

    def do(self):
        self.printDebugLog('[hbt2] 代码风格检查...')
        return SUCCESS if self.config.checkstyle or self.style_errors() == 0 else\
            '\nWARNING: You must fix the errors and warnings first, then post review again'

    def style_errors(self):
        hbt_dir = self.config.hbt_dir
        if platform.system().startswith(self.CYGWIN_SYSTEM_PREFIX):
            # change to cygwin path
            hbt_dir = subprocess.check_output('cygpath -m "' + self.config.hbt_dir + '"', shell=True).strip()

        jar_file = os.path.join(hbt_dir, self.CHECKSTYLE_JAR_FILE_NAME)
        config_file = os.path.join(hbt_dir, self.CHECKSTYLE_CONFIG_FILE_NAME)

        # check code command
        command = 'java -jar ' + jar_file + ' -c ' + config_file

        for f in self.get_committed():
            if f.check_style(command) != 0:
                return 1
        return 0


class RBTPostAction(Action):
    CHECKSTYLE_TAG = '[checked_5_0_4]'

    def do(self):
        args = self.context.params['rbt_args']
        rbt_command = 'rbt post ' + ' '.join(arg for arg in args)
        summary = self.commit_message.split('\n')[0].replace('"', '\\\"')
        if summary:
            rbt_command += ' --summary "%s %s"' % (self.CHECKSTYLE_TAG, summary)
        rbt_command = rbt_command.replace(' -s ', '')
        need_auto_open = rbt_command.find(' -o') > 0
        rbt_command = rbt_command.replace(' -o', '')
        if self.debug:
            rbt_command += ' -d'

        self.printDebugLog('[hbt2] ' + rbt_command)
        post_message = subprocess.check_output(rbt_command, shell=True)

        review_url, request_id = self.get_review_url(post_message.split('\n'))
        if not review_url:
            return u'WARNING: 没有找到review url信息'

        # 再次更新 review request 的描述以加入新增的 jira url 和 review request link 信息等
        if self.update_commit_message(review_url) == 0:
            rbt_command += ' -r ' + request_id
            if need_auto_open:
                rbt_command += ' -o'

            self.printDebugLog('[hbt2] ' + rbt_command)
            return SUCCESS if subprocess.call(rbt_command, shell=True) == 0 else\
                u'WARNING: rbt命令执行出错'

        return u'WARNING: 更新commit message失败'

    def update_commit_message(self, review_url):
        lines = []
        has_updated = False
        review_request_re = r'^\s*%s/r/(\d+)/\s*$'
        jira_link_re = r'^\s*%s/browse/.*\s*$'
        jira_link = '%s/browse/%s' % (self.config.jira_url, self.get_issue_id())

        for line in self.commit_message.split('\n'):
            if re.compile(review_request_re % self.config.reviewboard_url).match(line):
                lines.append(review_url)
                has_updated = True
            elif re.compile(jira_link_re % self.config.jira_url).match(line):
                lines.append(jira_link)
            else:
                lines.append(line.decode('utf-8'))

        if not has_updated:
            lines.append('')
            lines.append(review_url)
            lines.append(jira_link)
        new_message = '\n'.join(lines).replace('"', '\\\"')
        # update review board url to commit message
        return subprocess.call('git commit --amend -m "%s"' % new_message, shell=True)


class RBTAction(Action):
    def do(self):
        self.printDebugLog(u'[hbt2] 执行rbt...')
        args = self.context.params['rbt_args']
        rbt_command = 'rbt %s %s' % (self.context.info_name.encode('ascii', 'ignore'), ' '.join(arg for arg in args))
        if self.debug:
            rbt_command += ' -d'
        self.printDebugLog('[hbt2] ' + rbt_command)
        return SUCCESS if subprocess.call(rbt_command, shell=True) == 0 else\
            'WARNING: rbt命令执行出错'
