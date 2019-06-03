#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import webbrowser

import click

from php.composer import Composer
from util.output import Output

root_path = os.path.dirname(__file__)
current_path = os.getcwd()


class Context(object):
    pass


@click.group()
def main():
    pass


@main.command()
def greet():
    click.echo(click.style("Hello, glad to see You~!", fg="cyan"))


@main.group()
def composer():
    pass


@composer.command("ls")
@click.option("-f", "--file", help="path of composer.json file, default './composer.json'",
              default=Composer.FILE_DEFAULT, type=str)
@click.option("-p", "--display", help="the way of display", is_flag=True)
def composer_br_ls(file, display):
    data = Composer.reveal(file)
    repo = Composer.build_repo(data)
    for name, item in repo.items():
        if display:
            Output.notice(item.detail())
        else:
            Output.notice(item.short())


@composer.command("add")
@click.option("-f", "--file", help="path of composer.json file, default './composer.json'",
              default=Composer.FILE_DEFAULT, type=str)
@click.option("-n", "--name", help="lib name", required=True, type=str)
@click.option("-u", "--url", help="repo url", type=str)
@click.option("-t", "--type", help="repo type", default="git", type=click.Choice(["git", "vcs"]))
@click.option("-e", "--as_version", help="set as version", default="master", type=str)
@click.option("-b", "--branch", help="branch name", required=True, type=str)
def composer_br_add(file, name, url, type, as_version, branch):
    Composer.pre_check(name, url)

    data = Composer.reveal(file)
    item = {"name": name, "url": url, "type": type}
    if as_version is not None:
        item["as_version"] = as_version
    if branch is not None:
        item["branch"] = branch
    data = Composer.add(data, item)
    Composer.save(data, file, ".new")


@composer.command("del")
@click.option("-f", "--file", help="path of composer.json file, default './composer.json'",
              default=Composer.FILE_DEFAULT, type=str)
@click.option("-n", "--name", help="lib name", required=True, type=str)
@click.option("-u", "--url", help="repo url", required=True, type=str)
@click.option("-e", "--version", help="set as version, such as: 1.*", required=True, type=str)
def composer_br_del(file, name, url, version):
    Composer.pre_check(name, url)

    item = {"name": name, "url": url, "version": version}
    data = Composer.reveal(file)
    data = Composer.delete(data, item)
    Composer.save(data, file, ".new")


@composer.command("php-ver")
@click.option("-f", "--file", help="path of composer.json file, default './composer.json'",
              default=Composer.FILE_DEFAULT, type=str)
@click.option("-e", "--version", help="the version of php that composer",
              default=Composer.PHP_VERSION_DEFAULT, type=str)
def composer_php_version(file, version):
    data = Composer.reveal(file)
    data = Composer.set_php_version(data, version)
    Composer.save(data, file, ".new")


@composer.command("libmap")
def composer_lib():
    webbrowser.open(url="http://baidu.com", new=2)


def composer_didi():
    # os.commands('bash <(curl -s -S -L https://git.xiaojukeji.com/elevate/environment/raw/master/setup-scripts/composer-setup.sh)')
    pass
