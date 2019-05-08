"""
  Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.

  Permission is hereby granted, free of charge, to any person obtaining a copy of this
  software and associated documentation files (the "Software"), to deal in the Software
  without restriction, including without limitation the rights to use, copy, modify,
  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import six
from cfnlint import CloudFormationLintRule
from cfnlint import RuleMatch


class Configuration(CloudFormationLintRule):
    """Check Update Policy Configuration"""
    id = 'E3016'
    shortdesc = 'Check the configuration of a resources UpdatePolicy'
    description = 'Make sure a resources UpdatePolicy is properly configured'
    source_url = 'https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html'
    tags = ['resources', 'updatepolicy']
    valid_attributes = {
        'sub': {
            'AutoScalingReplacingUpdate': {
                'WillReplace': {
                    'PrimitiveType': 'Boolean'
                }
            },
            'AutoScalingRollingUpdate': {
                'MaxBatchSize': {
                    'PrimitiveType': 'Integer'
                },
                'MinInstancesInService': {
                    'PrimitiveType': 'Integer'
                },
                'MinSuccessfulInstancesPercent': {
                    'PrimitiveType': 'Integer'
                },
                'PauseTime': {
                    'PrimitiveType': 'String'
                },
                'SuspendProcesses': {
                    'PrimitiveType': 'List',
                    'ValidValues': [
                        'Launch', 'Terminate', 'HealthCheck',
                        'ReplaceUnhealthy', 'AZRebalance', 'AlarmNotification',
                        'ScheduledActions', 'AddToLoadBalancer'
                    ]
                },
                'WaitOnResourceSignals': {
                    'PrimitiveType': 'Boolean'
                }
            },
            'AutoScalingScheduledAction': {
                'IgnoreUnmodifiedGroupSizeProperties': {
                    'PrimitiveType': 'Boolean'
                }
            },
            'CodeDeployLambdaAliasUpdate': {
                'AfterAllowTrafficHook': {
                    'PrimitiveType': 'String'
                },
                'ApplicationName': {
                    'PrimitiveType': 'String'
                },
                'BeforeAllowTrafficHook': {
                    'PrimitiveType': 'String'
                },
                'DeploymentGroupName': {
                    'PrimitiveType': 'String'
                },
            }
        },
        'main': {
            'AutoScalingReplacingUpdate': {
                'Type': 'AutoScalingReplacingUpdate',
                'ResourceTypes': [
                    'AWS::AutoScaling::AutoScalingGroup'
                ]
            },
            'AutoScalingRollingUpdate': {
                'Type': 'AutoScalingRollingUpdate',
                'ResourceTypes': [
                    'AWS::AutoScaling::AutoScalingGroup'
                ]
            },
            'AutoScalingScheduledAction': {
                'Type': 'AutoScalingScheduledAction',
                'ResourceTypes': [
                    'AWS::AutoScaling::AutoScalingGroup'
                ]
            },
            'CodeDeployLambdaAliasUpdate': {
                'Type': 'CodeDeployLambdaAliasUpdate',
                'ResourceTypes': [
                    'AWS::Lambda::Alias'
                ]
            },
            'UseOnlineResharding': {
                'PrimitiveType': 'Boolean',
                'ResourceTypes': [
                    'AWS::ElastiCache::ReplicationGroup'
                ]
            }
        },
        'primitive_types': {
            'String': six.string_types,
            'Integer': int,
            'Boolean': bool,
            'List': list
        }
    }

    def check_value(self, value, path, **kwargs):
        """ Check a primitive value """
        matches = []

        prim_type = kwargs.get('primitive_type')
        if prim_type == 'List':
            valid_values = kwargs.get('valid_values')
            if valid_values:
                if value not in valid_values:
                    message = 'Allowed values for {0} are ({1})'
                    matches.append(
                        RuleMatch(path, message.format(kwargs.get('key_name'), ', '.join(map(str, valid_values)))))
        else:
            default_message = 'Value for {0} must be of type {1}'
            if not isinstance(value, self.valid_attributes.get('primitive_types').get(prim_type)):
                matches.append(
                    RuleMatch(path, default_message.format(kwargs.get('key_name'), prim_type)))

        return matches

    def check_attributes(self, cfn, properties, spec_type, path):
        """
            Check the properties against the spec
        """
        matches = []
        spec = self.valid_attributes.get('sub').get(spec_type)
        if isinstance(properties, dict):
            for p_value_safe, p_path_safe in properties.items_safe(path):
                for p_name, p_value in p_value_safe.items():
                    if p_name in spec:
                        up_type_spec = spec.get(p_name)
                        if 'Type' in up_type_spec:
                            matches.extend(
                                self.check_attributes(
                                    cfn, p_value, up_type_spec.get('Type'), p_path_safe[:] + [p_name]))
                        else:
                            matches.extend(
                                cfn.check_value(
                                    obj={p_name: p_value}, key=p_name, path=p_path_safe[:],
                                    check_value=self.check_value,
                                    valid_values=up_type_spec.get('ValidValues', []),
                                    primitive_type=up_type_spec.get('PrimitiveType'),
                                    key_name=p_name
                                )
                            )
                    else:
                        message = 'UpdatePolicy doesn\'t support type {0}'
                        matches.append(
                            RuleMatch(path[:] + [p_name], message.format(p_name)))
        else:
            message = '{0} should be an object'
            matches.append(
                RuleMatch(path, message.format(path[-1])))

        return matches

    def check_update_policy(self, cfn, update_policy, path, resource_type):
        """Check an update policy"""
        matches = []
        for up_type, up_value in update_policy.items():
            up_path = path[:] + [up_type]
            up_type_spec = self.valid_attributes.get('main').get(up_type)
            if up_type_spec:
                if resource_type not in up_type_spec.get('ResourceTypes'):
                    message = 'UpdatePolicy only supports this type for resources of type ({0})'
                    matches.append(
                        RuleMatch(up_path, message.format(', '.join(map(str, up_type_spec.get('ResourceTypes'))))))
                if 'Type' in up_type_spec:
                    matches.extend(
                        self.check_attributes(
                            cfn, up_value, up_type_spec.get('Type'), up_path[:]))

                else:
                    matches.extend(
                        cfn.check_value(
                            obj={up_type: up_value}, key=up_type, path=up_path[:],
                            check_value=self.check_value,
                            valid_values=up_type_spec.get('ValidValues', []),
                            primitive_type=up_type_spec.get('PrimitiveType'),
                            key_name=up_type
                        )
                    )
            else:
                message = 'UpdatePolicy doesn\'t support type {0}'
                matches.append(
                    RuleMatch(up_path, message.format(up_type)))

        return matches

    def match(self, cfn):
        """Check CloudFormation Resources"""

        matches = []

        for r_name, r_values in cfn.get_resources().items():
            update_policy = r_values.get('UpdatePolicy')
            if update_policy is None:
                continue
            resource_type = r_values.get('Type')
            if isinstance(update_policy, dict):
                path = ['Resources', r_name, 'UpdatePolicy']
                for up_value_safe, up_path_safe in update_policy.items_safe(path):
                    matches.extend(self.check_update_policy(cfn, up_value_safe, up_path_safe, resource_type))
            else:
                message = 'UpdatePolicy should be an object'
                matches.append(
                    RuleMatch(['Resources', r_name, 'UpdatePolicy'], message.format()))

        return matches
