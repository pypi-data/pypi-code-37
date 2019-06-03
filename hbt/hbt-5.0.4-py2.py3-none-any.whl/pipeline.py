#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import traceback
from actions import *


class InvalidCommitError(BaseException):
    """Raised if an invalid configuration is encountered."""

    def __init__(self, message):
        super(InvalidCommitError, self).__init__(message)

profile_rbt_land = 'land'
profile_rbt_post = 'post'
profile_rbt = 'rbt'
pipeline_rbt_land = [WorkspaceCleanAction, CommitCheckAction, LandCheckAction, PushAction, JiraUpdateAction, CloseReviewboardAction]
pipeline_rbt_post = [WorkspaceCleanAction, CommitCheckAction, CopyrightUpdateAction, StyleCheckAction, RbtPostArgsCheckAction, RBTPostAction]
pipeline_rbt = [RBTAction]

profiles = {
    profile_rbt_land: pipeline_rbt_land,
    profile_rbt_post: pipeline_rbt_post,
    profile_rbt: pipeline_rbt
}


class Pipeline(object):
    def __init__(self, config, ctx, actions_class):
        self.queue = []
        commit_message = subprocess.check_output('git log --format=%B -n 1', shell=True).strip()
        for action in actions_class:
            self.queue.append(action(config, ctx, commit_message))

    def run(self):
        for action in self.queue:
            try:
                err = action.do()
                if err:
                    print(err)
                    sys.exit(1)
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)

    @staticmethod
    def create_pipeline(config, ctx, profile):
        return Pipeline(config, ctx, profiles.get(profile))


if __name__ == '__main__':
    subject_re = r'^\s*(feat|fix|docs|style|refactor|chore)?\s*\((.*)\)\s*[:|：]\s*(.+)\n'
    new_line_re = r'\n'
    body_re = r'((?:.+\n)+)'
    affect_re = r'^([测试影响|影响].*)\n'

    msg = """feat(ANDROID_INFRA-57): 修改copyright后自动commit文件。消除手动commit的困扰。

扫描被修改的文件，发现copyright不对的，进行修改。然后自动提交commit相关改动。
扫描被修改的文件，发现copyright不对的，进行修改。然后自动提交commit相关改动。
扫描被修改的文件，发现copyright不对的，进行修改。然后自动提交commit相关改动。

测试影响： copyright 相关测试

rev
"""
    # print re.compile(subject_re + new_line_re + body_re + new_line_re + affect_re, re.MULTILINE).match(msg).group(2)
    print (re.compile(subject_re, re.MULTILINE).match(msg).group(2))
    pass
