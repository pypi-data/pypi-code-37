#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: opsgeniecli.py
#
# Copyright 2019 Yorick Hoorneman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for opsgeniecli

.. _Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html

"""
from datetime import timedelta
from datetime import datetime
from operator import itemgetter
import urllib.parse
import urllib.request
import os
import collections
import pathlib
import sys
import json
import requests
from prettytable import PrettyTable
import click
import pytz
from opsgenielib import OpsGenie, InvalidApiKey

__author__ = '''Yorick Hoorneman <yhoorneman@gmail.com>'''
__docformat__ = '''google'''
__date__ = '''26-02-2019'''
__copyright__ = '''Copyright 2019, Yorick Hoorneman'''
__credits__ = ["Yorick Hoorneman"]
__license__ = '''MIT'''
__maintainer__ = '''Yorick Hoorneman'''
__email__ = '''<yhoorneman@gmail.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

class MutuallyExclusiveOption(click.Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help = "" # pylint: disable=bad-option-value, redefined-builtin, unused-variable
        if self.mutually_exclusive:
            ex_str = ', '.join(self.mutually_exclusive)
            kwargs['help'] = (
                ' NOTE: This argument is mutually exclusive with '
                ' arguments: [' + ex_str + '].'
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise click.UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(
                    self.name,
                    ', '.join(self.mutually_exclusive)
                )
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(
            ctx,
            opts,
            args
        )

@click.group()
@click.pass_context
@click.option('--config', cls=MutuallyExclusiveOption,
              envvar='OPSGENIE_CONFIG',
              mutually_exclusive=["team", "apikey"])
@click.option('--teamname', cls=MutuallyExclusiveOption,
              envvar='OPSGENIE_TEAM',
              mutually_exclusive=["config"])
@click.option('--teamid', cls=MutuallyExclusiveOption,
              envvar='OPSGENIE_TEAM',
              mutually_exclusive=["config"])
@click.option('--apikey', cls=MutuallyExclusiveOption,
              envvar='OPSGENIE_APIKEY',
              mutually_exclusive=["config"])
@click.option('--profile')
def bootstrapper(context, config, teamname, teamid, apikey, profile):
    """
Auth:

    \b
    Location of the json formatted config file:
        - Set "OPSGENIE_CONFIG" as environment variable
            example: $export OPSGENIE_CONFIG='<location>'
        - Or use --config '<location>'

    \b
    Team name & api key:
        - Set "OPSGENIE_TEAM" and "OPSGENIE_APIKEY" as environment variables
        - Or us --team and --apikey
            example: --team team5 --apikey XXXXXX

Command line examples:

    \b
    $ opsgenie teams list
    $ opsgenie teams get -id xxxxxx
    $ opsgenie teams set xxxx
    """

    if not config and not teamname and not apikey and not teamid:
        config = pathlib.PurePath(pathlib.Path.home(), ".opsgenie-cli", "config.json")
        if os.path.isfile(config):
            with open(config) as config_file:
                data = json.load(config_file)
                if not profile:
                    profile = 'default'
                context.obj['teamname'] = data[0][profile]['teamname']
                context.obj['apikey'] = data[0][profile]['apikey']
                context.obj['teamid'] = data[0][profile]['teamid']
        else:
            raise click.UsageError(
                "No config was given. Do one of the following:\n"
                "\t-Create a config file at: ~/.opsgenie-cli/config.json\n"
                "\t-Specify a config file. Use --config or set the environment variable OPSGENIE_CONFIG\n"
                "\t-Specify the team & apikey. Use --team & --apikey or set the env vars OPSGENIE_TEAM & OPSGENIE_APIKEY"
            )
    elif config:
        with open(config) as config_file:
            data = json.load(config_file)
            if profile:
                context.obj['teamname'] = data[0][profile]['teamname']
                context.obj['apikey'] = data[0][profile]['apikey']
                context.obj['teamid'] = data[0][profile]['teamid']
            else:
                context.obj['teamname'] = data[0]['default']['teamname']
                context.obj['apikey'] = data[0]['default']['apikey']
                context.obj['teamid'] = data[0]['default']['teamid']
    elif teamname and apikey and teamid:
        context.obj['teamname'] = teamname
        context.obj['apikey'] = apikey
        context.obj['teamid'] = teamid
    try:
        context.obj['opsgenie'] = OpsGenie(f"{context.obj['apikey']}")
    except InvalidApiKey:
        raise SystemExit('I am sorry to say that the provided api key is invalid.')

@bootstrapper.group()
@click.pass_context
def alerts(context): # pylint: disable=unused-argument
    pass

@alerts.command(name='query')
@click.option('--query')
@click.pass_context
def alerts_query(context, query):
    result = context.obj['opsgenie'].query_alerts(query)
    format_table = PrettyTable(['message', 'tags', 'integration', 'createdAt'])
    for alert in result['data']:
        format_table.add_row([alert['message'], alert['tags'], alert['integration']['type'], alert['createdAt']])
    print(format_table)

@alerts.command(name='list')
@click.option('--active', default=False, is_flag=True)
@click.option('--moreinfo', default=False, is_flag=True)
@click.option('--teamname', default=False)
@click.option('--limit', default=50)
@click.pass_context
def alerts_list(context, active, limit, moreinfo, teamname):
    if {context.obj.get('teamname')} and not teamname:
        teamname = f"{context.obj.get('teamname')}"
    if not {context.obj.get('teamname')} and not teamname:
        raise click.UsageError(
            "Specify the teamname using --teamname."
        )
    result = context.obj['opsgenie'].list_alerts(teamname, limit)
    sortedlist = sorted(result['data'], key=itemgetter('status'))
    if moreinfo:
        format_table = PrettyTable(['id', 'name', 'status', 'acknowledged',
                                    'createdAt', 'tags', 'source', 'integration'])
    else:
        format_table = PrettyTable(['id', 'name', 'status', 'acknowledged', 'createdAt'])
    for item in sortedlist:
        if active:
            if item['status'] == 'open' and not item['acknowledged']: #item['acknowledged'] == False
                created_at = datetime.strptime(item['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
                if moreinfo:
                    format_table.add_row([item['id'], item['message'], item['status'], item['acknowledged'],
                                          created_at, item['tags'], item['source'], item['integration']['name']])
                else:
                    format_table.add_row([item['id'], item['message'], item['status'], item['acknowledged'], created_at])
        else:
            created_at = datetime.strptime(item['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
            if moreinfo:
                format_table.add_row([item['id'], item['message'], item['status'], item['acknowledged'],
                                      created_at, item['tags'], item['source'], item['integration']['name']])
            else:
                format_table.add_row([item['id'], item['message'], item['status'], item['acknowledged'], created_at])
    print(format_table)

@alerts.command(name='get')
@click.option('--id') # pylint: disable=redefined-builtin
@click.pass_context
def alerts_get(context, id): # pylint: disable=redefined-builtin, invalid-name
    result = context.obj['opsgenie'].get_alerts(id)
    print(json.dumps(result, indent=4, sort_keys=True))

@alerts.command(name='count')
@click.pass_context
def alerts_count(context):
    url = f"https://api.opsgenie.com/v2/alerts?limit=100&query=teams:{context.obj.get('teamname')}"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'Content-Type': "application/json"
        }
    response = requests.request("GET", url, headers=headers)
    parsed = json.loads(response.text)
    dictionary = collections.Counter(item['message'] for item in parsed['data'])
    sorted_by_count = sorted(dictionary.items(), reverse=True, key=itemgetter(1))
    for alert in sorted_by_count:
        print(f"{alert[1]} - {alert[0]}")

@alerts.command(name='acknowledge')
@click.option('--id', prompt=False, cls=MutuallyExclusiveOption, mutually_exclusive=["all"])
@click.option('--all', default=False, is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def alerts_acknowledge(context, id, all):  # pylint: disable=redefined-builtin, invalid-name
    if id:
        result = context.obj['opsgenie'].acknowledge_alerts(id)
        print(json.dumps(result, indent=4, sort_keys=True))
    elif all:
        result = context.obj['opsgenie'].query_alerts(f"teams:{context.obj.get('teamname')}")
        for item in result['data']:
            if item['status'] == 'open' and not item['acknowledged']:
                response = context.obj['opsgenie'].acknowledge_alerts(item['id'])
                if response['result'] == 'Request will be processed':
                    print(f"✓ - alert acknowledged: {item['id']} - {item['message']}")
                else:
                    print(f"x - alert Not acknowledged: {item['id']} - {item['message']}")

@bootstrapper.group()
@click.pass_context
def policy_alerts(context): # pylint: disable=unused-argument
    pass

@policy_alerts.command(name='list')
@click.option('--id', help='Specify the teamID for team-based alert policies instead of global policies.')
@click.pass_context
def policy_alerts_list(context, id): # pylint: disable=redefined-builtin, invalid-name
    if {context.obj.get('teamid')} and not id:
        id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not id:
        raise click.UsageError(
            "Specify the teamid using --id."
        )
    result = context.obj['opsgenie'].list_alert_policy(id)   #list_alerts(teamname, limit)
    format_table = PrettyTable(['id', 'name', 'enabled'])
    for item in result['data']:
        format_table.add_row([item['id'], item['name'], item['enabled']])
    print(format_table)

@policy_alerts.command(name='create')
@click.option('--state', type=click.Choice(['match-any-condition', 'match-all-conditions']), help='Choose if all condition should be met or atleast one.')
# @click.argument('--condition_one', nargs=4, help='field/operation/expectedValue or field/key/not(optional)/operation/expectedValue. \
#     Example: Message, contains, dynamodb. or Example2: extra-properties, host, not, regex, ^sbpojira.*$')
@click.option('--name', help='Specify the name of the alert policies.')
@click.pass_context
def policy_alerts_create(context, state, name):  # pylint: disable=redefined-builtin, invalid-name
    url = f"https://api.opsgenie.com/v2/policies?teamId={context.obj.get('teamid')}"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        }
    body = {
        "type":"alert",
        "description":f"{name}",
        "enabled":"true",
        "filter":{
            "type":f"{state}",
            "conditions": [
                {
                    "field": "extra-properties",
                    "key": "host",
                    "not": "true",
                    "operation": "starts-with",
                    "expectedValue": "expected3"
                }
            ]
        },
        "name":f"{name}",
        "message":"{{message}}",
        "tags":["filtered"],
        "alertDescription":"{{description}}"
    }
    response = requests.post(url, headers=headers, json=body)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))

@policy_alerts.command(name='delete')
@click.option('--id', help='The id of the alerts policy that will be deleted.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["all"])
@click.option('--all', default=False, is_flag=True, help='Will remove all alerts policies for the team.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.option('--teamid', help='Specify the team id.')
@click.pass_context
def policy_alerts_delete(context, id, all, teamid): # pylint: disable=redefined-builtin, invalid-name
    if {context.obj.get('teamid')} and not teamid:
        teamid = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not teamid:
        raise click.UsageError(
            "Specify the teamid using --teamid."
        )
    if id:
        response = context.obj['opsgenie'].delete_alert_policy(id, teamid)
        if response['result'] == 'Deleted':
            print(f"alert policy {id} deleted for team: {context.obj.get('teamname')}")
        else:
            print(response.text)
            sys.exit(1)
    if all:
        reponse = context.obj['opsgenie'].list_alert_policy(teamid)
        print("The following alerts policies will be deleted:")
        for item in reponse['data']:
            print(f"{item['id']} - {item['name']}")
        value = click.confirm('\nDo you want to continue?', abort=True)
        if value:
            for item in reponse['data']:
                response = context.obj['opsgenie'].delete_alert_policy(f"{item['id']}", teamid)
                if response['result'] == 'Deleted':
                    print(f"alert policy {item['id']} deleted for team: {context.obj.get('teamname')}")
                else:
                    print(response.text)
                    sys.exit(1)

@bootstrapper.group()
@click.pass_context
def integrations(context): # pylint: disable=unused-argument
    pass

@integrations.command(name='list')
@click.option('--id', cls=MutuallyExclusiveOption, mutually_exclusive=["teamname"])
@click.option('--teamname', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def integrations_list(context, id, teamname): # pylint: disable=redefined-builtin, invalid-name
    if id:
        result = context.obj['opsgenie'].list_integrations_by_team_id(id)
    elif teamname:
        result = context.obj['opsgenie'].list_integrations_by_team_name(teamname)
    else:
        raise click.UsageError(
            "Specify the team name or tema id using --teamname or --id."
        )
    format_table = PrettyTable(['type', 'id', 'name', 'teamId', 'enabled'])
    for item in result['data']:
        format_table.add_row([item['type'], item['id'], item['name'], item['teamId'], item['enabled']])
    print(format_table)

@integrations.command(name='get')
@click.option('--id', required=True) # pylint: disable=redefined-builtin
@click.pass_context
def integrations_get(context, id): # pylint: disable=redefined-builtin, invalid-name
    result = context.obj['opsgenie'].get_integrations(id)
    print(json.dumps(result, indent=4, sort_keys=True))

@bootstrapper.group()
@click.pass_context
def config(context): # pylint: disable=unused-argument
    pass

@config.command(name='list') # pylint: disable=undefined-variable
@click.option('--config', default="~/.opsgenie-cli/config.json", envvar='OPSGENIE_CONFIG')
def config_list(config): # pylint: disable=redefined-outer-name
    if "~" in config:
        config = os.path.expanduser(config)
    with open(config) as config_file:
        data = json.load(config_file)
        for i in data[0]:
            print(json.dumps(i, indent=4, sort_keys=True))

@bootstrapper.group()
@click.pass_context
def policy_maintenance(context): # pylint: disable=unused-argument
    pass

@policy_maintenance.command(name='get')
@click.option('--id', prompt=True)
@click.pass_context
def policy_maintenance_get(context, id): # pylint: disable=redefined-builtin, invalid-name
    result = context.obj['opsgenie'].get_maintenance_policy(id)
    print(json.dumps(result, indent=4, sort_keys=True))

@policy_maintenance.command(name='set')
@click.option('--description', prompt=True)
@click.option('--startdate', help='Example: 2019-03-15T14:34:09Z')
@click.option('--enddate', help='Example: 2019-03-15T15:34:09Z')
@click.option('--filter', cls=MutuallyExclusiveOption, mutually_exclusive=["id"], help='Filter down based on the name of the alert policy.')
@click.option('--id', cls=MutuallyExclusiveOption, mutually_exclusive=["filter"], help='The id of the entity that maintenance will be applied.') # pylint: disable=redefined-builtin, invalid-name
@click.option('--state', type=click.Choice(['enabled', 'disabled']), default='enabled', help='State of rule that \
    will be defined in maintenance and can take \
    either enabled or disabled for policy type rules. This field has to be disabled for integration type entity rules')
@click.option('--entity', type=click.Choice(['integration', 'policy']), default='policy', help='The type of the entity \
    that maintenance will be applied. It can be either integration or policy')
@click.option('--hours', type=int, help='Filter duration is hours.')
@click.pass_context
def policy_maintenance_set(context, description, id, state, entity, hours, filter, startdate, enddate):  # pylint: disable=redefined-builtin, invalid-name
    if not filter and not id:
        raise click.UsageError("--id or --filter is required")
    if filter:
        result = context.obj['opsgenie'].list_alert_policy(context.obj.get('teamid'))
        filtered_results = [x for x in result['data'] if filter in x['name']]
        if len(filtered_results) == 1:
            id = filtered_results[0]['id']
        else:
            print(f"\nMultiple (alert or notification) filters found for {filter}.")
            filtered_format_table = PrettyTable(['id', 'name', 'type', 'enabled'])
            for result in filtered_results:
                filtered_format_table.add_row([result['id'], result['name'], result['type'], result['enabled']])
            print(filtered_format_table)
            id = ""
            while len(id) < 30:
                id = click.prompt('Enter the ID of the filter you want to use', type=str)
            print(id)
    if startdate and enddate:
        start = datetime.strptime(startdate, "%Y-%m-%dT%H:%M:%SZ")
        end = datetime.strptime(enddate, "%Y-%m-%dT%H:%M:%SZ")
        startdatetime = start.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        enddatetime = end.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        start = datetime.now().astimezone(pytz.utc)
        end = start + timedelta(hours=hours)
    if hours:
        result = context.obj['opsgenie'].set_maintenance_policy_hours(context.obj.get('teamid'), hours, id, entity, description, state)
    if startdate and enddate:
        result = context.obj['opsgenie'].set_maintenance_policy_schedule(context.obj.get('teamid'), startdate, enddate, entity, id, description, state)
    if result.status_code == 201:
        if hours:
            print(f"✓ - Maintenance policy created.\n\tDescription: {description}\n\tTime: {hours}hours")
        if startdate and enddate:
            startdatetime = start.strftime('%Y-%m-%d %H:%M:%S')
            enddatetime = end.strftime('%Y-%m-%d %H:%M:%S')
            print(f"✓ - Maintenance policy created.\n\tDescription: {description}\n\tTime: from {startdatetime} - {enddatetime}")

@policy_maintenance.command(name='cancel')
@click.option('--maintenanceid', prompt=True)
@click.pass_context
def policy_maintenance_cancel(context, maintenanceid):  # pylint: disable=redefined-builtin, invalid-name
        result = context.obj['opsgenie'].cancel_maintenance_policy(maintenanceid)
        print(json.dumps(result, indent=4, sort_keys=True))

@policy_maintenance.command(name='delete')
@click.option('--id', help='The id of the maintenance policy that will be deleted.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["all"])
@click.option('--all', default=False, is_flag=True, help='Will remove all maintenance policies for the team.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.option('--teamid', required=True)
@click.pass_context
def policy_maintenance_delete(context, id, all, teamid): # pylint: disable=redefined-builtin, invalid-name
    # headers = {
    #     'Authorization': f"GenieKey {context.obj.get('apikey')}",
    # }
    if all:
        # url = "https://api.opsgenie.com/v1/maintenance?teamId={context.obj.get('teamid')}"
        # response = requests.request("GET", url, headers=headers)
        # parsed = json.loads(response.text)
        result = context.obj['opsgenie'].list_maintenance_policy(teamid)
        print("The following maintenance policies will be deleted:")
        for item in result['data']:
            print(f"{item['id']} - {item['description']}")
        value = click.confirm('\nDo you want to continue?', abort=True)
        if value:
            for item in result['data']:
                # url = f"https://api.opsgenie.com/v1/maintenance/{item['id']}"
                # response = requests.request("DELETE", url, headers=headers)
                result = context.obj['opsgenie'].delete_maintenance_policy(item['id'])
                if result.status_code == 200:
                    print(f"✓ - maintenance policy {item['id']} deleted for team: {context.obj.get('teamname')}")
    elif id:
        # url = f"https://api.opsgenie.com/v1/maintenance/{id}"
        # response = requests.request("DELETE", url, headers=headers)
        result = context.obj['opsgenie'].delete_maintenance_policy(id)
        if result.status_code == 200:
            print(f"✓ - maintenance policy {id} deleted for team: {context.obj.get('teamname')}")
        else:
            print(result.text)
            sys.exit(1)
    else:
        raise click.UsageError(
            "Use --id to specify one maintenance ID to remove or --all "
        )

@policy_maintenance.command(name='list')
@click.option('--nonexpired', '--active', default=False, is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["past"])
@click.option('--past', default=False, is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["non-expired"])
@click.option('--teamid', required=True)
@click.pass_context
def policy_maintenance_list(context, nonexpired, past, teamid):
    if nonexpired:
        result = context.obj['opsgenie'].list_maintenance_policy_non_expired(teamid)
    elif past:
        result = context.obj['opsgenie'].list_maintenance_policy_past(teamid)
    else:
        result = context.obj['opsgenie'].list_maintenance_policy(teamid)
    format_table = PrettyTable(['id', 'status', 'description', 'type', 'Startdate'])
    for item in result['data']:
        format_table.add_row([item['id'], item['status'], item['description'],
                              item['time']['type'], item['time']['startDate']])
    print(format_table)

@bootstrapper.group()
@click.pass_context
def heartbeat(context):  # pylint: disable=unused-argument
    pass

@heartbeat.command(name='ping')
@click.option('--heartbeatname', help='The name of the heartbeat.')
@click.pass_context
def heartbeat_ping(context, heartbeatname):  # pylint: disable=redefined-builtin, invalid-name
    result = context.obj['opsgenie'].ping_heartbeat(heartbeatname)
    print(json.dumps(result, indent=4, sort_keys=True))

@heartbeat.command(name='get')
@click.option('--heartbeatname', help='The name of the heartbeat.')
@click.pass_context
def heartbeat_get(context, heartbeatname):  # pylint: disable=redefined-builtin, invalid-name
    result = context.obj['opsgenie'].get_heartbeat(heartbeatname)
    print(json.dumps(result, indent=4, sort_keys=True))

@heartbeat.command(name='list')
@click.pass_context
def heartbeat_list(context):  # pylint: disable=redefined-builtin, invalid-name
    result = context.obj['opsgenie'].list_heartbeats()
    print(json.dumps(result, indent=4, sort_keys=True))

@heartbeat.command(name='enable')
@click.option('--heartbeatname', help='The name of the heartbeat.')
@click.pass_context
def heartbeat_enable(context, heartbeatname):  # pylint: disable=redefined-builtin, invalid-name
    result = context.obj['opsgenie'].enable_heartbeat(heartbeatname)
    print(json.dumps(result, indent=4, sort_keys=True))

@heartbeat.command(name='disable')
@click.option('--heartbeatname', help='The name of the heartbeat.')
@click.pass_context
def heartbeat_disable(context, heartbeatname):  # pylint: disable=redefined-builtin, invalid-name
    result = context.obj['opsgenie'].disable_heartbeat(heartbeatname)
    print(json.dumps(result, indent=4, sort_keys=True))

@bootstrapper.group()
def teams():
    pass

@teams.command(name='get')
@click.option('--id', cls=MutuallyExclusiveOption, mutually_exclusive=["teamname"])
@click.option('--teamname', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def teams_get(context, id, teamname):  # pylint: disable=redefined-builtin, invalid-name
    if id:
        result = context.obj['opsgenie'].get_team_by_id(id)
    elif teamname:
        result = context.obj['opsgenie'].get_team_by_name(teamname)
    format_table = PrettyTable([result['data']['name'] + ' ids', result['data']['name'] + ' usernames'])
    for item in result['data']['members']:
        format_table.add_row([item['user']['id'], item['user']['username']])
    print(format_table)

@teams.command(name='logs')
@click.option('--id', cls=MutuallyExclusiveOption, mutually_exclusive=["teamname"])
@click.option('--teamname', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def teams_logs(context, id, teamname):  # pylint: disable=redefined-builtin, invalid-name
    if {context.obj.get('teamname')} and not teamname:
        teamname = f"{context.obj.get('teamname')}"
    if not {context.obj.get('teamname')} and not {context.obj.get('id')} and not teamname and not id:
        raise click.UsageError(
            "Specify the teamname using --teamname or team id using --id."
        )
    if id:
        result = context.obj['opsgenie'].get_team_logs_by_id(id)
    elif teamname:
        result = context.obj['opsgenie'].get_team_logs_by_name(teamname)
    print(json.dumps(result, indent=4, sort_keys=True))

@teams.command(name='list')
@click.pass_context
def teams_list(context):
    result = context.obj['opsgenie'].list_teams()
    format_table = PrettyTable(['id', 'name'])
    for item in result['data']:
        format_table.add_row([item['id'], item['name']])
    print(format_table)

@bootstrapper.group()
def teams_routing_rules():
    pass

@teams_routing_rules.command(name='list')
@click.option('--id', cls=MutuallyExclusiveOption, mutually_exclusive=["teamname"])
@click.option('--teamname', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def teams_routing_list(context, id, teamname): # pylint: disable=redefined-builtin, invalid-name
    if id:
        result = context.obj['opsgenie'].get_routing_rules_by_id(id)
    elif teamname:
        result = context.obj['opsgenie'].get_routing_rules_by_name(teamname)
    else:
        raise click.UsageError(
            "No team id or team name was specified. Use --id or --teamname.\n"
        )
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache",
        }
    print(json.dumps(result, indent=4, sort_keys=True))

@bootstrapper.group()
def escalations():
    pass

@escalations.command(name='get')
@click.option('--id', cls=MutuallyExclusiveOption, mutually_exclusive=["escalationname"])
@click.option('--escalationname', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def escalations_get(context, id, escalationname): # pylint: disable=redefined-builtin, invalid-name
    if id:
        result = context.obj['opsgenie'].get_escalations_by_id(id)
    elif escalationname:
        result = context.obj['opsgenie'].get_escalations_by_name(escalationname)
    else:
        raise click.UsageError(
            "No escalation id or escalation name was specified. Use --id or --escalationname.\n"
        )
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache",
        }
    print(json.dumps(result, indent=4, sort_keys=True))

@escalations.command(name='list')
@click.pass_context
def escalations_list(context):
    result = context.obj['opsgenie'].list_escalations()
    format_table = PrettyTable(['id', 'name', 'ownerTeam'])
    for item in result['data']:
        format_table.add_row([item['id'], item['name'], item['ownerTeam']['name']])
    print(format_table)

@bootstrapper.group()
@click.pass_context
def schedules(context): # pylint: disable=unused-argument
    pass

@schedules.command(name='get')
@click.option('--id', cls=MutuallyExclusiveOption, mutually_exclusive=["schedulename"])
@click.option('--schedulename', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def schedules_get(context, id, schedulename):  # pylint: disable=redefined-builtin, invalid-name
    if id:
        result = context.obj['opsgenie'].get_schedules_by_id(id)
    elif schedulename:
        result = context.obj['opsgenie'].get_schedules_by_name(schedulename)
    else:
        raise click.UsageError(
            "No schedule id or schedule name was specified. Use --id or --schedulename.\n"
        )
    print(json.dumps(result, indent=4, sort_keys=True))

@schedules.command(name='list')
@click.pass_context
def schedules_list(context):
    result = context.obj['opsgenie'].list_schedules()
    sortedlist = sorted(result['data'], key=itemgetter('name'))
    format_table = PrettyTable(['id', 'name'])
    for item in sortedlist:
        format_table.add_row([item['id'], item['name']])
    print(format_table)

@bootstrapper.group()
@click.pass_context
def logs(context): # pylint: disable=unused-argument
    pass

@logs.command(name='download')
@click.option('--marker', required=True)
@click.option('--downloadpath', required=True)
@click.option('--limit')
@click.pass_context
def logs_download(context, marker, limit, downloadpath):
    if limit and marker:
        result = context.obj['opsgenie'].get_logs_filenames(marker, limit)
    if marker and not limit:
        result = context.obj['opsgenie'].get_logs_filenames(marker)
    else:
        raise click.UsageError(
            "No schedule id or schedule name was specified. Use --id or --schedulename.\n"
        )
    result = context.obj['opsgenie'].get_logs_filenames(id)
    total_count = len(result['data'])
    current_count = 1
    for file in result['data']:
        print(f"{current_count} - {total_count} - downloading {file['filename']}")
        download_url = context.obj['opsgenie'].get_logs_download_link(file['filename'])
        urllib.request.urlretrieve(download_url.text, f"{downloadpath}/{file['filename']}")
        current_count = current_count + 1

@bootstrapper.group()
@click.pass_context
def policy_notifications(context): # pylint: disable=unused-argument
    pass

@policy_notifications.command(name='get')
@click.option('--id', prompt=True)
@click.option('--teamid')
@click.pass_context
def policy_notifications_get(context, id, teamid): # pylint: disable=redefined-builtin, invalid-name
    if teamid:
        result = context.obj['opsgenie'].get_notification_policy(id, teamid)
    elif context.obj.get('teamid') and not teamid:
        result = context.obj['opsgenie'].get_notification_policy(id, context.obj.get('teamid'))
    else:
        raise click.UsageError(
            "No team id was found. Use --teamid or specify the team id in the config file.\n"
        )
    print(json.dumps(result, indent=4, sort_keys=True))

@policy_notifications.command(name='delete')
@click.option('--id', help='The id of the notifications policy that will be deleted.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["all"])
@click.option('--all', default=False, is_flag=True, help='Will remove all notifications policies for the team.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.option('--teamid')
@click.pass_context
def policy_notifications_delete(context, id, teamid, all): # pylint: disable=redefined-builtin, invalid-name
    if id:
        if teamid:
            result = context.obj['opsgenie'].get_notification_policy(id, teamid)
        elif context.obj.get('teamid'):
            result = context.obj['opsgenie'].delete_notification_policy(id, context.obj.get('teamid'))
        else:
            raise click.UsageError(
                "No team id was found. Use --teamid or specify the team id in the config file.\n"
            )

        if result.status_code == 200:
            print(f"✓ - notification policy {id} deleted for team: {context.obj.get('teamname')}")
        else:
            print(result.text)
            sys.exit(1)

    if all:
        if teamid:
            result = context.obj['opsgenie'].list_notification_policy(teamid)
        elif context.obj.get('teamid') and not teamid:
            result = context.obj['opsgenie'].list_notification_policy(context.obj.get('teamid'))
        else:
            raise click.UsageError(
                "No team id was found. Use --teamid or specify the team id in the config file.\n"
            )
        print("The following notifications policies will be deleted:")
        for item in result['data']:
            print(f"{item['id']} - {item['name']}")
        value = click.confirm('\nDo you want to continue?', abort=True)
        if value:
            for item in result['data']:
                if teamid:
                    result = context.obj['opsgenie'].delete_notification_policy(item['id'], teamid)
                elif context.obj.get('teamid') and not teamid:
                    result = context.obj['opsgenie'].delete_notification_policy(item['id'], context.obj.get('teamid'))
                if result.status_code == 200:
                    print(f"notifications policy {item['id']} deleted for team: {context.obj.get('teamname')}")
                else:
                    print(result.text)
                    sys.exit(1)

@policy_notifications.command(name='list')
@click.option('--teamid', help='Specify a teamID. The teamID from the config is used when no --teamid argument is given.')
@click.option('--nonexpired', '--active', default=False, is_flag=True)
@click.pass_context
def policy_notifications_list(context, teamid, nonexpired): # pylint: disable=redefined-builtin, invalid-name
    if teamid:
        result = context.obj['opsgenie'].list_notification_policy(teamid)
    elif context.obj.get('teamid') and not teamid:
        result = context.obj['opsgenie'].list_notification_policy(context.obj.get('teamid'))
    else:
        raise click.UsageError(
            "No team id was found. Use --id or specify the team id in the config file.\n"
        )
    sortedlist = sorted(result['data'], key=itemgetter('name'))
    format_table = PrettyTable(['id', 'name', 'enabled'])
    for item in sortedlist:
        if nonexpired:
            if item['enabled']:
                format_table.add_row([item['id'], item['name'], item['enabled']])
        else:
            format_table.add_row([item['id'], item['name'], item['enabled']])
    print(format_table)

@bootstrapper.command()
@click.pass_context
def on_call(context):
    result = context.obj['opsgenie'].get_users_on_call()
    table_eod = PrettyTable(['Team', 'EOD'])
    table_no_eod = PrettyTable(['Opsgenie teams without an EOD'])
    for item in result['data']:
        if item['onCallParticipants']:
            table_eod.add_row([item['_parent']['name'], item['onCallParticipants'][0]['name']])
        else:
            table_no_eod.add_row([item['_parent']['name']])
    print(table_no_eod)
    print(table_eod)

@bootstrapper.command()
@click.option('--startdate', cls=MutuallyExclusiveOption, mutually_exclusive=["hours"],
              help='Example: 2019-03-15T14:34:09Z.')
@click.option('--enddate', cls=MutuallyExclusiveOption, mutually_exclusive=["hours"],
              help='Example: 2019-03-15T15:34:09Z')
@click.option('--teamname')
@click.option('--engineer', help='Name the username of the engineer who will be on call.')
@click.option('--hours', type=int, help='Amount of hours to set the override for.')
@click.pass_context
def override(context, teamname, engineer, hours, startdate, enddate): # pylint: disable=redefined-builtin, invalid-name
    """
    Examples:

    \b
    $ opsgeniecli.py override --teamname <TEAMSCHEDULE> --engineer <ENGINEER> --hours <INTEGER>
    $ opsgeniecli.py override --teamname <TEAMSCHEDULE> --engineer <ENGINEER> \
        --startdate 2019-03-15T14:34:09Z --enddate 2019-03-15T15:34:09Z
    """
    if hours:
        result = context.obj['opsgenie'].set_override_for_hours(teamname, engineer, hours)
        output_start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        output_end_date = (datetime.now() + timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M:%S')
    elif startdate and enddate:
        result = context.obj['opsgenie'].set_override_scheduled(teamname, startdate, enddate, engineer)
        start = datetime.strptime(startdate, "%Y-%m-%dT%H:%M:%SZ")
        end = datetime.strptime(enddate, "%Y-%m-%dT%H:%M:%SZ")
        output_start_date = start.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
        output_end_date = end.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
    else:
        raise click.UsageError(
            "Specify the amount of hours you want to override the schedule (using --hours), \
            or specify a schedule (using --startdate and --enddate)."
        )
    if result.status_code == 201:
        print(f"✓ - override set to {engineer} between {output_start_date} and {output_end_date}")
    else:
        print(result.text)

def main():
    """Main entry point of tool"""
    bootstrapper(obj={})  # pylint: disable=no-value-for-parameter, unexpected-keyword-arg

if __name__ == '__main__':
    main()
