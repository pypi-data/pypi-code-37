import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-transfer", "0.33.0", __name__, "aws-transfer@0.33.0.jsii.tgz")
class CfnServer(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-transfer.CfnServer"):
    """A CloudFormation ``AWS::Transfer::Server``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html
    cloudformationResource:
        AWS::Transfer::Server
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, endpoint_details: typing.Optional[typing.Union[typing.Optional["EndpointDetailsProperty"], typing.Optional[aws_cdk.cdk.Token]]]=None, endpoint_type: typing.Optional[str]=None, identity_provider_details: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["IdentityProviderDetailsProperty"]]]=None, identity_provider_type: typing.Optional[str]=None, logging_role: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::Transfer::Server``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            endpointDetails: ``AWS::Transfer::Server.EndpointDetails``.
            endpointType: ``AWS::Transfer::Server.EndpointType``.
            identityProviderDetails: ``AWS::Transfer::Server.IdentityProviderDetails``.
            identityProviderType: ``AWS::Transfer::Server.IdentityProviderType``.
            loggingRole: ``AWS::Transfer::Server.LoggingRole``.
            tags: ``AWS::Transfer::Server.Tags``.
        """
        props: CfnServerProps = {}

        if endpoint_details is not None:
            props["endpointDetails"] = endpoint_details

        if endpoint_type is not None:
            props["endpointType"] = endpoint_type

        if identity_provider_details is not None:
            props["identityProviderDetails"] = identity_provider_details

        if identity_provider_type is not None:
            props["identityProviderType"] = identity_provider_type

        if logging_role is not None:
            props["loggingRole"] = logging_role

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnServer, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            properties: -
        """
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnServerProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="serverArn")
    def server_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "serverArn")

    @property
    @jsii.member(jsii_name="serverId")
    def server_id(self) -> str:
        """
        cloudformationAttribute:
            ServerId
        """
        return jsii.get(self, "serverId")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        """The ``TagManager`` handles setting, removing and formatting tags.

        Tags should be managed either passing them as properties during
        initiation or by calling methods on this object. If both techniques are
        used only the tags from the TagManager will be used. ``Tag`` (aspect)
        will use the manager.
        """
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-transfer.CfnServer.EndpointDetailsProperty", jsii_struct_bases=[])
    class EndpointDetailsProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html
        """
        vpcEndpointId: str
        """``CfnServer.EndpointDetailsProperty.VpcEndpointId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-vpcendpointid
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-transfer.CfnServer.IdentityProviderDetailsProperty", jsii_struct_bases=[])
    class IdentityProviderDetailsProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html
        """
        invocationRole: str
        """``CfnServer.IdentityProviderDetailsProperty.InvocationRole``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-invocationrole
        """

        url: str
        """``CfnServer.IdentityProviderDetailsProperty.Url``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-url
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-transfer.CfnServerProps", jsii_struct_bases=[])
class CfnServerProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::Transfer::Server``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html
    """
    endpointDetails: typing.Union["CfnServer.EndpointDetailsProperty", aws_cdk.cdk.Token]
    """``AWS::Transfer::Server.EndpointDetails``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointdetails
    """

    endpointType: str
    """``AWS::Transfer::Server.EndpointType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointtype
    """

    identityProviderDetails: typing.Union[aws_cdk.cdk.Token, "CfnServer.IdentityProviderDetailsProperty"]
    """``AWS::Transfer::Server.IdentityProviderDetails``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityproviderdetails
    """

    identityProviderType: str
    """``AWS::Transfer::Server.IdentityProviderType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityprovidertype
    """

    loggingRole: str
    """``AWS::Transfer::Server.LoggingRole``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-loggingrole
    """

    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::Transfer::Server.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-tags
    """

class CfnUser(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-transfer.CfnUser"):
    """A CloudFormation ``AWS::Transfer::User``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html
    cloudformationResource:
        AWS::Transfer::User
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, role: str, server_id: str, user_name: str, home_directory: typing.Optional[str]=None, policy: typing.Optional[str]=None, ssh_public_keys: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::Transfer::User``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            role: ``AWS::Transfer::User.Role``.
            serverId: ``AWS::Transfer::User.ServerId``.
            userName: ``AWS::Transfer::User.UserName``.
            homeDirectory: ``AWS::Transfer::User.HomeDirectory``.
            policy: ``AWS::Transfer::User.Policy``.
            sshPublicKeys: ``AWS::Transfer::User.SshPublicKeys``.
            tags: ``AWS::Transfer::User.Tags``.
        """
        props: CfnUserProps = {"role": role, "serverId": server_id, "userName": user_name}

        if home_directory is not None:
            props["homeDirectory"] = home_directory

        if policy is not None:
            props["policy"] = policy

        if ssh_public_keys is not None:
            props["sshPublicKeys"] = ssh_public_keys

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnUser, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            properties: -
        """
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnUserProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        """The ``TagManager`` handles setting, removing and formatting tags.

        Tags should be managed either passing them as properties during
        initiation or by calling methods on this object. If both techniques are
        used only the tags from the TagManager will be used. ``Tag`` (aspect)
        will use the manager.
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="userArn")
    def user_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "userArn")

    @property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> str:
        """
        cloudformationAttribute:
            UserName
        """
        return jsii.get(self, "userName")

    @property
    @jsii.member(jsii_name="userServerId")
    def user_server_id(self) -> str:
        """
        cloudformationAttribute:
            ServerId
        """
        return jsii.get(self, "userServerId")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnUserProps(jsii.compat.TypedDict, total=False):
    homeDirectory: str
    """``AWS::Transfer::User.HomeDirectory``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectory
    """
    policy: str
    """``AWS::Transfer::User.Policy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-policy
    """
    sshPublicKeys: typing.List[str]
    """``AWS::Transfer::User.SshPublicKeys``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-sshpublickeys
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::Transfer::User.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-transfer.CfnUserProps", jsii_struct_bases=[_CfnUserProps])
class CfnUserProps(_CfnUserProps):
    """Properties for defining a ``AWS::Transfer::User``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html
    """
    role: str
    """``AWS::Transfer::User.Role``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-role
    """

    serverId: str
    """``AWS::Transfer::User.ServerId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-serverid
    """

    userName: str
    """``AWS::Transfer::User.UserName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-username
    """

__all__ = ["CfnServer", "CfnServerProps", "CfnUser", "CfnUserProps", "__jsii_assembly__"]

publication.publish()
