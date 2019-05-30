import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/cx-api", "0.33.0", __name__, "cx-api@0.33.0.jsii.tgz")
@jsii.data_type_optionals(jsii_struct_bases=[])
class _Artifact(jsii.compat.TypedDict, total=False):
    autoDeploy: bool
    dependencies: typing.List[str]
    metadata: typing.Mapping[str,typing.List["MetadataEntry"]]
    missing: typing.Mapping[str,"MissingContext"]
    properties: typing.Mapping[str,typing.Any]

@jsii.data_type(jsii_type="@aws-cdk/cx-api.Artifact", jsii_struct_bases=[_Artifact])
class Artifact(_Artifact):
    environment: str

    type: "ArtifactType"

@jsii.enum(jsii_type="@aws-cdk/cx-api.ArtifactType")
class ArtifactType(enum.Enum):
    None_ = "None"
    AwsCloudFormationStack = "AwsCloudFormationStack"

@jsii.data_type_optionals(jsii_struct_bases=[])
class _AssemblyManifest(jsii.compat.TypedDict, total=False):
    artifacts: typing.Mapping[str,"Artifact"]
    """The set of artifacts in this assembly."""
    runtime: "RuntimeInfo"
    """Runtime information."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.AssemblyManifest", jsii_struct_bases=[_AssemblyManifest])
class AssemblyManifest(_AssemblyManifest):
    version: str
    """Protocol version."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.AvailabilityZonesContextQuery", jsii_struct_bases=[])
class AvailabilityZonesContextQuery(jsii.compat.TypedDict, total=False):
    """Query to hosted zone context provider."""
    account: str
    """Query account."""

    region: str
    """Query region."""

@jsii.data_type_optionals(jsii_struct_bases=[])
class _AwsCloudFormationStackProperties(jsii.compat.TypedDict, total=False):
    parameters: typing.Mapping[str,str]

@jsii.data_type(jsii_type="@aws-cdk/cx-api.AwsCloudFormationStackProperties", jsii_struct_bases=[_AwsCloudFormationStackProperties])
class AwsCloudFormationStackProperties(_AwsCloudFormationStackProperties):
    templateFile: str

@jsii.data_type(jsii_type="@aws-cdk/cx-api.BuildOptions", jsii_struct_bases=[])
class BuildOptions(jsii.compat.TypedDict, total=False):
    runtimeInfo: "RuntimeInfo"
    """Include runtime information (module versions) in manifest.

    Default:
        true
    """

class CloudArtifact(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cx-api.CloudArtifact"):
    def __init__(self, assembly: "CloudAssembly", id: str, *, environment: str, type: "ArtifactType", auto_deploy: typing.Optional[bool]=None, dependencies: typing.Optional[typing.List[str]]=None, metadata: typing.Optional[typing.Mapping[str,typing.List["MetadataEntry"]]]=None, missing: typing.Optional[typing.Mapping[str,"MissingContext"]]=None, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        """
        Arguments:
            assembly: -
            id: -
            artifact: -
            environment: -
            type: -
            autoDeploy: -
            dependencies: -
            metadata: -
            missing: -
            properties: -
        """
        artifact: Artifact = {"environment": environment, "type": type}

        if auto_deploy is not None:
            artifact["autoDeploy"] = auto_deploy

        if dependencies is not None:
            artifact["dependencies"] = dependencies

        if metadata is not None:
            artifact["metadata"] = metadata

        if missing is not None:
            artifact["missing"] = missing

        if properties is not None:
            artifact["properties"] = properties

        jsii.create(CloudArtifact, self, [assembly, id, artifact])

    @jsii.member(jsii_name="from")
    @classmethod
    def from_(cls, assembly: "CloudAssembly", name: str, *, environment: str, type: "ArtifactType", auto_deploy: typing.Optional[bool]=None, dependencies: typing.Optional[typing.List[str]]=None, metadata: typing.Optional[typing.Mapping[str,typing.List["MetadataEntry"]]]=None, missing: typing.Optional[typing.Mapping[str,"MissingContext"]]=None, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> "CloudArtifact":
        """
        Arguments:
            assembly: -
            name: -
            artifact: -
            environment: -
            type: -
            autoDeploy: -
            dependencies: -
            metadata: -
            missing: -
            properties: -
        """
        artifact: Artifact = {"environment": environment, "type": type}

        if auto_deploy is not None:
            artifact["autoDeploy"] = auto_deploy

        if dependencies is not None:
            artifact["dependencies"] = dependencies

        if metadata is not None:
            artifact["metadata"] = metadata

        if missing is not None:
            artifact["missing"] = missing

        if properties is not None:
            artifact["properties"] = properties

        return jsii.sinvoke(cls, "from", [assembly, name, artifact])

    @property
    @jsii.member(jsii_name="assembly")
    def assembly(self) -> "CloudAssembly":
        return jsii.get(self, "assembly")

    @property
    @jsii.member(jsii_name="autoDeploy")
    def auto_deploy(self) -> bool:
        return jsii.get(self, "autoDeploy")

    @property
    @jsii.member(jsii_name="depends")
    def depends(self) -> typing.List["CloudArtifact"]:
        return jsii.get(self, "depends")

    @property
    @jsii.member(jsii_name="dependsIDs")
    def depends_i_ds(self) -> typing.List[str]:
        return jsii.get(self, "dependsIDs")

    @property
    @jsii.member(jsii_name="environment")
    def environment(self) -> "Environment":
        return jsii.get(self, "environment")

    @property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        return jsii.get(self, "id")

    @property
    @jsii.member(jsii_name="messages")
    def messages(self) -> typing.List["SynthesisMessage"]:
        return jsii.get(self, "messages")

    @property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[str,typing.List["MetadataEntry"]]:
        return jsii.get(self, "metadata")

    @property
    @jsii.member(jsii_name="missing")
    def missing(self) -> typing.Mapping[str,"MissingContext"]:
        return jsii.get(self, "missing")

    @property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "properties")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "ArtifactType":
        return jsii.get(self, "type")


class CloudAssembly(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cx-api.CloudAssembly"):
    def __init__(self, directory: str) -> None:
        """
        Arguments:
            directory: -
        """
        jsii.create(CloudAssembly, self, [directory])

    @jsii.member(jsii_name="getStack")
    def get_stack(self, id: str) -> "CloudFormationStackArtifact":
        """
        Arguments:
            id: -
        """
        return jsii.invoke(self, "getStack", [id])

    @jsii.member(jsii_name="readJson")
    def read_json(self, file_path: str) -> typing.Any:
        """
        Arguments:
            filePath: -
        """
        return jsii.invoke(self, "readJson", [file_path])

    @jsii.member(jsii_name="tryGetArtifact")
    def try_get_artifact(self, id: str) -> typing.Optional["CloudArtifact"]:
        """
        Arguments:
            id: -
        """
        return jsii.invoke(self, "tryGetArtifact", [id])

    @property
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> typing.List["CloudArtifact"]:
        return jsii.get(self, "artifacts")

    @property
    @jsii.member(jsii_name="directory")
    def directory(self) -> str:
        return jsii.get(self, "directory")

    @property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> "AssemblyManifest":
        return jsii.get(self, "manifest")

    @property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> "RuntimeInfo":
        return jsii.get(self, "runtime")

    @property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List["CloudFormationStackArtifact"]:
        return jsii.get(self, "stacks")

    @property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        return jsii.get(self, "version")

    @property
    @jsii.member(jsii_name="missing")
    def missing(self) -> typing.Optional[typing.Mapping[str,"MissingContext"]]:
        return jsii.get(self, "missing")


class CloudAssemblyBuilder(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cx-api.CloudAssemblyBuilder"):
    def __init__(self, outdir: typing.Optional[str]=None) -> None:
        """
        Arguments:
            outdir: -
        """
        jsii.create(CloudAssemblyBuilder, self, [outdir])

    @jsii.member(jsii_name="addArtifact")
    def add_artifact(self, name: str, *, environment: str, type: "ArtifactType", auto_deploy: typing.Optional[bool]=None, dependencies: typing.Optional[typing.List[str]]=None, metadata: typing.Optional[typing.Mapping[str,typing.List["MetadataEntry"]]]=None, missing: typing.Optional[typing.Mapping[str,"MissingContext"]]=None, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        """
        Arguments:
            name: -
            artifact: -
            environment: -
            type: -
            autoDeploy: -
            dependencies: -
            metadata: -
            missing: -
            properties: -
        """
        artifact: Artifact = {"environment": environment, "type": type}

        if auto_deploy is not None:
            artifact["autoDeploy"] = auto_deploy

        if dependencies is not None:
            artifact["dependencies"] = dependencies

        if metadata is not None:
            artifact["metadata"] = metadata

        if missing is not None:
            artifact["missing"] = missing

        if properties is not None:
            artifact["properties"] = properties

        return jsii.invoke(self, "addArtifact", [name, artifact])

    @jsii.member(jsii_name="build")
    def build(self, *, runtime_info: typing.Optional["RuntimeInfo"]=None) -> "CloudAssembly":
        """
        Arguments:
            options: -
            runtimeInfo: Include runtime information (module versions) in manifest. Default: true
        """
        options: BuildOptions = {}

        if runtime_info is not None:
            options["runtimeInfo"] = runtime_info

        return jsii.invoke(self, "build", [options])

    @property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> str:
        return jsii.get(self, "outdir")


class CloudFormationStackArtifact(CloudArtifact, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cx-api.CloudFormationStackArtifact"):
    def __init__(self, assembly: "CloudAssembly", name: str, *, environment: str, type: "ArtifactType", auto_deploy: typing.Optional[bool]=None, dependencies: typing.Optional[typing.List[str]]=None, metadata: typing.Optional[typing.Mapping[str,typing.List["MetadataEntry"]]]=None, missing: typing.Optional[typing.Mapping[str,"MissingContext"]]=None, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        """
        Arguments:
            assembly: -
            name: -
            artifact: -
            environment: -
            type: -
            autoDeploy: -
            dependencies: -
            metadata: -
            missing: -
            properties: -
        """
        artifact: Artifact = {"environment": environment, "type": type}

        if auto_deploy is not None:
            artifact["autoDeploy"] = auto_deploy

        if dependencies is not None:
            artifact["dependencies"] = dependencies

        if metadata is not None:
            artifact["metadata"] = metadata

        if missing is not None:
            artifact["missing"] = missing

        if properties is not None:
            artifact["properties"] = properties

        jsii.create(CloudFormationStackArtifact, self, [assembly, name, artifact])

    @property
    @jsii.member(jsii_name="assets")
    def assets(self) -> typing.List[typing.Union["FileAssetMetadataEntry", "ContainerImageAssetMetadataEntry"]]:
        return jsii.get(self, "assets")

    @property
    @jsii.member(jsii_name="logicalIdToPathMap")
    def logical_id_to_path_map(self) -> typing.Mapping[str,str]:
        return jsii.get(self, "logicalIdToPathMap")

    @property
    @jsii.member(jsii_name="originalName")
    def original_name(self) -> str:
        return jsii.get(self, "originalName")

    @property
    @jsii.member(jsii_name="template")
    def template(self) -> typing.Any:
        return jsii.get(self, "template")

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        return jsii.set(self, "name", value)


@jsii.data_type_optionals(jsii_struct_bases=[])
class _ContainerImageAssetMetadataEntry(jsii.compat.TypedDict, total=False):
    buildArgs: typing.Mapping[str,str]
    """Build args to pass to the ``docker build`` command.

    Default:
        no build args are passed
    """
    repositoryName: str
    """ECR repository name, if omitted a default name based on the asset's ID is used instead.

    Specify this property if you need to statically
    address the image, e.g. from a Kubernetes Pod.
    Note, this is only the repository name, without the registry and
    the tag parts.

    Default:
        automatically derived from the asset's ID.
    """

@jsii.data_type(jsii_type="@aws-cdk/cx-api.ContainerImageAssetMetadataEntry", jsii_struct_bases=[_ContainerImageAssetMetadataEntry])
class ContainerImageAssetMetadataEntry(_ContainerImageAssetMetadataEntry):
    id: str
    """Logical identifier for the asset."""

    imageNameParameter: str
    """ECR Repository name and repo digest (separated by "@sha256:") where this image is stored."""

    packaging: str
    """Type of asset."""

    path: str
    """Path on disk to the asset."""

    sourceHash: str
    """The hash of the source directory used to build the asset."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.Environment", jsii_struct_bases=[])
class Environment(jsii.compat.TypedDict):
    """Models an AWS execution environment, for use within the CDK toolkit."""
    account: str
    """The 12-digit AWS account ID for the account this environment deploys into."""

    name: str
    """The arbitrary name of this environment (user-set, or at least user-meaningful)."""

    region: str
    """The AWS region name where this environment deploys into."""

class EnvironmentUtils(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cx-api.EnvironmentUtils"):
    def __init__(self) -> None:
        jsii.create(EnvironmentUtils, self, [])

    @jsii.member(jsii_name="format")
    @classmethod
    def format(cls, account: str, region: str) -> str:
        """
        Arguments:
            account: -
            region: -
        """
        return jsii.sinvoke(cls, "format", [account, region])

    @jsii.member(jsii_name="parse")
    @classmethod
    def parse(cls, environment: str) -> "Environment":
        """
        Arguments:
            environment: -
        """
        return jsii.sinvoke(cls, "parse", [environment])


@jsii.data_type(jsii_type="@aws-cdk/cx-api.FileAssetMetadataEntry", jsii_struct_bases=[])
class FileAssetMetadataEntry(jsii.compat.TypedDict):
    artifactHashParameter: str
    """The name of the parameter where the hash of the bundled asset should be passed in."""

    id: str
    """Logical identifier for the asset."""

    packaging: str
    """Requested packaging style."""

    path: str
    """Path on disk to the asset."""

    s3BucketParameter: str
    """Name of parameter where S3 bucket should be passed in."""

    s3KeyParameter: str
    """Name of parameter where S3 key should be passed in."""

    sourceHash: str
    """The hash of the source directory used to build the asset."""

@jsii.data_type_optionals(jsii_struct_bases=[])
class _HostedZoneContextQuery(jsii.compat.TypedDict, total=False):
    account: str
    """Query account."""
    privateZone: bool
    """True if the zone you want to find is a private hosted zone."""
    region: str
    """Query region."""
    vpcId: str
    """The VPC ID to that the private zone must be associated with.

    If you provide VPC ID and privateZone is false, this will return no results
    and raise an error.
    """

@jsii.data_type(jsii_type="@aws-cdk/cx-api.HostedZoneContextQuery", jsii_struct_bases=[_HostedZoneContextQuery])
class HostedZoneContextQuery(_HostedZoneContextQuery):
    """Query to hosted zone context provider."""
    domainName: str
    """The domain name e.g. example.com to lookup."""

@jsii.data_type_optionals(jsii_struct_bases=[])
class _MetadataEntry(jsii.compat.TypedDict, total=False):
    data: typing.Any
    """The data."""
    trace: typing.List[str]
    """A stack trace for when the entry was created."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.MetadataEntry", jsii_struct_bases=[_MetadataEntry])
class MetadataEntry(_MetadataEntry):
    """An metadata entry in the construct."""
    type: str
    """The type of the metadata entry."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.MissingContext", jsii_struct_bases=[])
class MissingContext(jsii.compat.TypedDict):
    """Represents a missing piece of context."""
    props: typing.Mapping[str,typing.Any]

    provider: str

@jsii.data_type(jsii_type="@aws-cdk/cx-api.RuntimeInfo", jsii_struct_bases=[])
class RuntimeInfo(jsii.compat.TypedDict):
    """Information about the application's runtime components."""
    libraries: typing.Mapping[str,str]
    """The list of libraries loaded in the application, associated with their versions."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.SSMParameterContextQuery", jsii_struct_bases=[])
class SSMParameterContextQuery(jsii.compat.TypedDict, total=False):
    """Query to hosted zone context provider."""
    account: str
    """Query account."""

    parameterName: str
    """Parameter name to query."""

    region: str
    """Query region."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.SynthesisMessage", jsii_struct_bases=[])
class SynthesisMessage(jsii.compat.TypedDict):
    entry: "MetadataEntry"

    id: str

    level: "SynthesisMessageLevel"

@jsii.enum(jsii_type="@aws-cdk/cx-api.SynthesisMessageLevel")
class SynthesisMessageLevel(enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

@jsii.data_type_optionals(jsii_struct_bases=[])
class _VpcContextQuery(jsii.compat.TypedDict, total=False):
    account: str
    """Query account."""
    region: str
    """Query region."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.VpcContextQuery", jsii_struct_bases=[_VpcContextQuery])
class VpcContextQuery(_VpcContextQuery):
    """Query input for looking up a VPC."""
    filter: typing.Mapping[str,str]
    """Filters to apply to the VPC.

    Filter parameters are the same as passed to DescribeVpcs.

    See:
        https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcs.html
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _VpcContextResponse(jsii.compat.TypedDict, total=False):
    isolatedSubnetIds: typing.List[str]
    """IDs of all isolated subnets.

    Element count: #(availabilityZones) · #(isolatedGroups)
    """
    isolatedSubnetNames: typing.List[str]
    """Name of isolated subnet groups.

    Element count: #(isolatedGroups)
    """
    privateSubnetIds: typing.List[str]
    """IDs of all private subnets.

    Element count: #(availabilityZones) · #(privateGroups)
    """
    privateSubnetNames: typing.List[str]
    """Name of private subnet groups.

    Element count: #(privateGroups)
    """
    publicSubnetIds: typing.List[str]
    """IDs of all public subnets.

    Element count: #(availabilityZones) · #(publicGroups)
    """
    publicSubnetNames: typing.List[str]
    """Name of public subnet groups.

    Element count: #(publicGroups)
    """
    vpnGatewayId: str
    """The VPN gateway ID."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.VpcContextResponse", jsii_struct_bases=[_VpcContextResponse])
class VpcContextResponse(_VpcContextResponse):
    """Properties of a discovered VPC."""
    availabilityZones: typing.List[str]
    """AZs."""

    vpcId: str
    """VPC id."""

__all__ = ["Artifact", "ArtifactType", "AssemblyManifest", "AvailabilityZonesContextQuery", "AwsCloudFormationStackProperties", "BuildOptions", "CloudArtifact", "CloudAssembly", "CloudAssemblyBuilder", "CloudFormationStackArtifact", "ContainerImageAssetMetadataEntry", "Environment", "EnvironmentUtils", "FileAssetMetadataEntry", "HostedZoneContextQuery", "MetadataEntry", "MissingContext", "RuntimeInfo", "SSMParameterContextQuery", "SynthesisMessage", "SynthesisMessageLevel", "VpcContextQuery", "VpcContextResponse", "__jsii_assembly__"]

publication.publish()
