import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_applicationautoscaling
import aws_cdk.aws_certificatemanager
import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_events
import aws_cdk.aws_events_targets
import aws_cdk.aws_iam
import aws_cdk.aws_route53
import aws_cdk.aws_route53_targets
import aws_cdk.aws_sqs
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ecs-patterns", "0.33.0", __name__, "aws-ecs-patterns@0.33.0.jsii.tgz")
class LoadBalancedFargateServiceApplet(aws_cdk.cdk.Stack, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancedFargateServiceApplet"):
    """An applet for a LoadBalancedFargateService.

    Sets up a Fargate service, Application
    load balancer, ECS cluster, VPC, and (optionally) Route53 alias record.
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, image: str, certificate: typing.Optional[str]=None, container_port: typing.Optional[jsii.Number]=None, cpu: typing.Optional[str]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, memory_mi_b: typing.Optional[str]=None, public_load_balancer: typing.Optional[bool]=None, public_tasks: typing.Optional[bool]=None, auto_deploy: typing.Optional[bool]=None, env: typing.Optional[aws_cdk.cdk.Environment]=None, naming_scheme: typing.Optional[aws_cdk.cdk.IAddressingScheme]=None, stack_name: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            image: The image to start (from DockerHub).
            certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443. Default: - No certificate associated with the load balancer.
            containerPort: The container port of the application load balancer attached to your Fargate service. Corresponds to container port mapping. Default: 80
            cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments. This default is set in the underlying FargateTaskDefinition construct. Default: 256
            desiredCount: Number of desired copies of running tasks. Default: 1
            domainName: Domain name for the service, e.g. api.example.com. Default: - No domain name.
            domainZone: Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
            environment: Environment variables to pass to the container. Default: - No environment variables.
            memoryMiB: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU) 1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU) 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU) Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU) Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
            publicLoadBalancer: Determines whether the Application Load Balancer will be internet-facing. Default: true
            publicTasks: Determines whether your Fargate Service will be assigned a public IP address. Default: false
            autoDeploy: Should the Stack be deployed when running ``cdk deploy`` without arguments (and listed when running ``cdk synth`` without arguments). Setting this to ``false`` is useful when you have a Stack in your CDK app that you don't want to deploy using the CDK toolkit - for example, because you're planning on deploying it through CodePipeline. Default: true
            env: The AWS environment (account/region) where this stack will be deployed. Default: - The ``default-account`` and ``default-region`` context parameters will be used. If they are undefined, it will not be possible to deploy the stack.
            namingScheme: Strategy for logical ID generation. Default: - The HashedNamingScheme will be used.
            stackName: Name to deploy the stack with. Default: - Derived from construct path.
        """
        props: LoadBalancedFargateServiceAppletProps = {"image": image}

        if certificate is not None:
            props["certificate"] = certificate

        if container_port is not None:
            props["containerPort"] = container_port

        if cpu is not None:
            props["cpu"] = cpu

        if desired_count is not None:
            props["desiredCount"] = desired_count

        if domain_name is not None:
            props["domainName"] = domain_name

        if domain_zone is not None:
            props["domainZone"] = domain_zone

        if environment is not None:
            props["environment"] = environment

        if memory_mi_b is not None:
            props["memoryMiB"] = memory_mi_b

        if public_load_balancer is not None:
            props["publicLoadBalancer"] = public_load_balancer

        if public_tasks is not None:
            props["publicTasks"] = public_tasks

        if auto_deploy is not None:
            props["autoDeploy"] = auto_deploy

        if env is not None:
            props["env"] = env

        if naming_scheme is not None:
            props["namingScheme"] = naming_scheme

        if stack_name is not None:
            props["stackName"] = stack_name

        jsii.create(LoadBalancedFargateServiceApplet, self, [scope, id, props])


@jsii.data_type_optionals(jsii_struct_bases=[aws_cdk.cdk.StackProps])
class _LoadBalancedFargateServiceAppletProps(aws_cdk.cdk.StackProps, jsii.compat.TypedDict, total=False):
    certificate: str
    """Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443.

    Default:
        - No certificate associated with the load balancer.
    """
    containerPort: jsii.Number
    """The container port of the application load balancer attached to your Fargate service.

    Corresponds to container port mapping.

    Default:
        80
    """
    cpu: str
    """The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments.

    This default is set in the underlying FargateTaskDefinition construct.

    Default:
        256
    """
    desiredCount: jsii.Number
    """Number of desired copies of running tasks.

    Default:
        1
    """
    domainName: str
    """Domain name for the service, e.g. api.example.com.

    Default:
        - No domain name.
    """
    domainZone: str
    """Route53 hosted zone for the domain, e.g. "example.com.".

    Default:
        - No Route53 hosted domain zone.
    """
    environment: typing.Mapping[str,str]
    """Environment variables to pass to the container.

    Default:
        - No environment variables.
    """
    memoryMiB: str
    """The amount (in MiB) of memory used by the task.

    This field is required and you must use one of the following values, which determines your range of valid values
    for the cpu parameter:

    0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU)

    1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU)

    2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU)

    Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU)

    Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU)

    This default is set in the underlying FargateTaskDefinition construct.

    Default:
        512
    """
    publicLoadBalancer: bool
    """Determines whether the Application Load Balancer will be internet-facing.

    Default:
        true
    """
    publicTasks: bool
    """Determines whether your Fargate Service will be assigned a public IP address.

    Default:
        false
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancedFargateServiceAppletProps", jsii_struct_bases=[_LoadBalancedFargateServiceAppletProps])
class LoadBalancedFargateServiceAppletProps(_LoadBalancedFargateServiceAppletProps):
    """Properties for a LoadBalancedEcsServiceApplet."""
    image: str
    """The image to start (from DockerHub)."""

class LoadBalancedServiceBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancedServiceBase"):
    """Base class for load-balanced Fargate and ECS service."""
    @staticmethod
    def __jsii_proxy_class__():
        return _LoadBalancedServiceBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, container_port: typing.Optional[jsii.Number]=None, desired_count: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, load_balancer_type: typing.Optional["LoadBalancerType"]=None, public_load_balancer: typing.Optional[bool]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            cluster: The cluster where your service will be deployed.
            image: The image to start.
            certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443. Default: - No certificate associated with the load balancer.
            containerPort: The container port of the application load balancer attached to your Fargate service. Corresponds to container port mapping. Default: 80
            desiredCount: Number of desired copies of running tasks. Default: 1
            environment: Environment variables to pass to the container. Default: - No environment variables.
            loadBalancerType: Whether to create an application load balancer or a network load balancer. Default: application
            publicLoadBalancer: Determines whether the Application Load Balancer will be internet-facing. Default: true
        """
        props: LoadBalancedServiceBaseProps = {"cluster": cluster, "image": image}

        if certificate is not None:
            props["certificate"] = certificate

        if container_port is not None:
            props["containerPort"] = container_port

        if desired_count is not None:
            props["desiredCount"] = desired_count

        if environment is not None:
            props["environment"] = environment

        if load_balancer_type is not None:
            props["loadBalancerType"] = load_balancer_type

        if public_load_balancer is not None:
            props["publicLoadBalancer"] = public_load_balancer

        jsii.create(LoadBalancedServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="addServiceAsTarget")
    def _add_service_as_target(self, service: aws_cdk.aws_ecs.BaseService) -> None:
        """
        Arguments:
            service: -
        """
        return jsii.invoke(self, "addServiceAsTarget", [service])

    @property
    @jsii.member(jsii_name="listener")
    def listener(self) -> typing.Union[aws_cdk.aws_elasticloadbalancingv2.ApplicationListener, aws_cdk.aws_elasticloadbalancingv2.NetworkListener]:
        return jsii.get(self, "listener")

    @property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> aws_cdk.aws_elasticloadbalancingv2.BaseLoadBalancer:
        return jsii.get(self, "loadBalancer")

    @property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> "LoadBalancerType":
        return jsii.get(self, "loadBalancerType")

    @property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> typing.Union[aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup, aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroup]:
        return jsii.get(self, "targetGroup")


class _LoadBalancedServiceBaseProxy(LoadBalancedServiceBase):
    pass

class LoadBalancedEc2Service(LoadBalancedServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancedEc2Service"):
    """A single task running on an ECS cluster fronted by a load balancer."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, memory_limit_mi_b: typing.Optional[jsii.Number]=None, memory_reservation_mi_b: typing.Optional[jsii.Number]=None, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, container_port: typing.Optional[jsii.Number]=None, desired_count: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, load_balancer_type: typing.Optional["LoadBalancerType"]=None, public_load_balancer: typing.Optional[bool]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            memoryLimitMiB: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
            memoryReservationMiB: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.
            cluster: The cluster where your service will be deployed.
            image: The image to start.
            certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443. Default: - No certificate associated with the load balancer.
            containerPort: The container port of the application load balancer attached to your Fargate service. Corresponds to container port mapping. Default: 80
            desiredCount: Number of desired copies of running tasks. Default: 1
            environment: Environment variables to pass to the container. Default: - No environment variables.
            loadBalancerType: Whether to create an application load balancer or a network load balancer. Default: application
            publicLoadBalancer: Determines whether the Application Load Balancer will be internet-facing. Default: true
        """
        props: LoadBalancedEc2ServiceProps = {"cluster": cluster, "image": image}

        if memory_limit_mi_b is not None:
            props["memoryLimitMiB"] = memory_limit_mi_b

        if memory_reservation_mi_b is not None:
            props["memoryReservationMiB"] = memory_reservation_mi_b

        if certificate is not None:
            props["certificate"] = certificate

        if container_port is not None:
            props["containerPort"] = container_port

        if desired_count is not None:
            props["desiredCount"] = desired_count

        if environment is not None:
            props["environment"] = environment

        if load_balancer_type is not None:
            props["loadBalancerType"] = load_balancer_type

        if public_load_balancer is not None:
            props["publicLoadBalancer"] = public_load_balancer

        jsii.create(LoadBalancedEc2Service, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.Ec2Service:
        """The ECS service in this construct."""
        return jsii.get(self, "service")


class LoadBalancedFargateService(LoadBalancedServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancedFargateService"):
    """A Fargate service running on an ECS cluster fronted by a load balancer."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cpu: typing.Optional[str]=None, create_logs: typing.Optional[bool]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, memory_mi_b: typing.Optional[str]=None, public_tasks: typing.Optional[bool]=None, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, container_port: typing.Optional[jsii.Number]=None, desired_count: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, load_balancer_type: typing.Optional["LoadBalancerType"]=None, public_load_balancer: typing.Optional[bool]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments. This default is set in the underlying FargateTaskDefinition construct. Default: 256
            createLogs: Whether to create an AWS log driver. Default: true
            domainName: Domain name for the service, e.g. api.example.com. Default: - No domain name.
            domainZone: Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
            memoryMiB: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU) 1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU) 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU) Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU) Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
            publicTasks: Determines whether your Fargate Service will be assigned a public IP address. Default: false
            cluster: The cluster where your service will be deployed.
            image: The image to start.
            certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443. Default: - No certificate associated with the load balancer.
            containerPort: The container port of the application load balancer attached to your Fargate service. Corresponds to container port mapping. Default: 80
            desiredCount: Number of desired copies of running tasks. Default: 1
            environment: Environment variables to pass to the container. Default: - No environment variables.
            loadBalancerType: Whether to create an application load balancer or a network load balancer. Default: application
            publicLoadBalancer: Determines whether the Application Load Balancer will be internet-facing. Default: true
        """
        props: LoadBalancedFargateServiceProps = {"cluster": cluster, "image": image}

        if cpu is not None:
            props["cpu"] = cpu

        if create_logs is not None:
            props["createLogs"] = create_logs

        if domain_name is not None:
            props["domainName"] = domain_name

        if domain_zone is not None:
            props["domainZone"] = domain_zone

        if memory_mi_b is not None:
            props["memoryMiB"] = memory_mi_b

        if public_tasks is not None:
            props["publicTasks"] = public_tasks

        if certificate is not None:
            props["certificate"] = certificate

        if container_port is not None:
            props["containerPort"] = container_port

        if desired_count is not None:
            props["desiredCount"] = desired_count

        if environment is not None:
            props["environment"] = environment

        if load_balancer_type is not None:
            props["loadBalancerType"] = load_balancer_type

        if public_load_balancer is not None:
            props["publicLoadBalancer"] = public_load_balancer

        jsii.create(LoadBalancedFargateService, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.FargateService:
        """The Fargate service in this construct."""
        return jsii.get(self, "service")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _LoadBalancedServiceBaseProps(jsii.compat.TypedDict, total=False):
    certificate: aws_cdk.aws_certificatemanager.ICertificate
    """Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443.

    Default:
        - No certificate associated with the load balancer.
    """
    containerPort: jsii.Number
    """The container port of the application load balancer attached to your Fargate service.

    Corresponds to container port mapping.

    Default:
        80
    """
    desiredCount: jsii.Number
    """Number of desired copies of running tasks.

    Default:
        1
    """
    environment: typing.Mapping[str,str]
    """Environment variables to pass to the container.

    Default:
        - No environment variables.
    """
    loadBalancerType: "LoadBalancerType"
    """Whether to create an application load balancer or a network load balancer.

    Default:
        application
    """
    publicLoadBalancer: bool
    """Determines whether the Application Load Balancer will be internet-facing.

    Default:
        true
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancedServiceBaseProps", jsii_struct_bases=[_LoadBalancedServiceBaseProps])
class LoadBalancedServiceBaseProps(_LoadBalancedServiceBaseProps):
    cluster: aws_cdk.aws_ecs.ICluster
    """The cluster where your service will be deployed."""

    image: aws_cdk.aws_ecs.ContainerImage
    """The image to start."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancedEc2ServiceProps", jsii_struct_bases=[LoadBalancedServiceBaseProps])
class LoadBalancedEc2ServiceProps(LoadBalancedServiceBaseProps, jsii.compat.TypedDict, total=False):
    """Properties for a LoadBalancedEc2Service."""
    memoryLimitMiB: jsii.Number
    """The hard limit (in MiB) of memory to present to the container.

    If your container attempts to exceed the allocated memory, the container
    is terminated.

    At least one of memoryLimitMiB and memoryReservationMiB is required.

    Default:
        - No memory limit.
    """

    memoryReservationMiB: jsii.Number
    """The soft limit (in MiB) of memory to reserve for the container.

    When system memory is under contention, Docker attempts to keep the
    container memory within the limit. If the container requires more memory,
    it can consume up to the value specified by the Memory property or all of
    the available memory on the container instance—whichever comes first.

    At least one of memoryLimitMiB and memoryReservationMiB is required.

    Default:
        - No memory reserved.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancedFargateServiceProps", jsii_struct_bases=[LoadBalancedServiceBaseProps])
class LoadBalancedFargateServiceProps(LoadBalancedServiceBaseProps, jsii.compat.TypedDict, total=False):
    """Properties for a LoadBalancedEcsService."""
    cpu: str
    """The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments.

    This default is set in the underlying FargateTaskDefinition construct.

    Default:
        256
    """

    createLogs: bool
    """Whether to create an AWS log driver.

    Default:
        true
    """

    domainName: str
    """Domain name for the service, e.g. api.example.com.

    Default:
        - No domain name.
    """

    domainZone: aws_cdk.aws_route53.IHostedZone
    """Route53 hosted zone for the domain, e.g. "example.com.".

    Default:
        - No Route53 hosted domain zone.
    """

    memoryMiB: str
    """The amount (in MiB) of memory used by the task.

    This field is required and you must use one of the following values, which determines your range of valid values
    for the cpu parameter:

    0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU)

    1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU)

    2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU)

    Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU)

    Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU)

    This default is set in the underlying FargateTaskDefinition construct.

    Default:
        512
    """

    publicTasks: bool
    """Determines whether your Fargate Service will be assigned a public IP address.

    Default:
        false
    """

@jsii.enum(jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancerType")
class LoadBalancerType(enum.Enum):
    Application = "Application"
    Network = "Network"

class QueueWorkerServiceBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs-patterns.QueueWorkerServiceBase"):
    """Base class for a Fargate and ECS queue worker service."""
    @staticmethod
    def __jsii_proxy_class__():
        return _QueueWorkerServiceBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            cluster: Cluster where service will be deployed.
            image: The image to start.
            command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
            desiredTaskCount: Number of desired copies of running tasks. Default: 1
            enableLogging: Flag to indicate whether to enable logging. Default: true
            environment: The environment variables to pass to the container. Default: 'QUEUE_NAME: queue.queueName'
            maxScalingCapacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
            queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. Default: 'SQSQueue with CloudFormation-generated name'
            scalingSteps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        """
        props: QueueWorkerServiceBaseProps = {"cluster": cluster, "image": image}

        if command is not None:
            props["command"] = command

        if desired_task_count is not None:
            props["desiredTaskCount"] = desired_task_count

        if enable_logging is not None:
            props["enableLogging"] = enable_logging

        if environment is not None:
            props["environment"] = environment

        if max_scaling_capacity is not None:
            props["maxScalingCapacity"] = max_scaling_capacity

        if queue is not None:
            props["queue"] = queue

        if scaling_steps is not None:
            props["scalingSteps"] = scaling_steps

        jsii.create(QueueWorkerServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="configureAutoscalingForService")
    def _configure_autoscaling_for_service(self, service: aws_cdk.aws_ecs.BaseService) -> None:
        """Configure autoscaling based off of CPU utilization as well as the number of messages visible in the SQS queue.

        Arguments:
            service: the ECS/Fargate service for which to apply the autoscaling rules to.
        """
        return jsii.invoke(self, "configureAutoscalingForService", [service])

    @property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        """The minimum number of tasks to run."""
        return jsii.get(self, "desiredCount")

    @property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[str,str]:
        """Environment variables that will include the queue name."""
        return jsii.get(self, "environment")

    @property
    @jsii.member(jsii_name="maxCapacity")
    def max_capacity(self) -> jsii.Number:
        """The maximum number of instances for autoscaling to scale up to."""
        return jsii.get(self, "maxCapacity")

    @property
    @jsii.member(jsii_name="scalingSteps")
    def scaling_steps(self) -> typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]:
        """The scaling interval for autoscaling based off an SQS Queue size."""
        return jsii.get(self, "scalingSteps")

    @property
    @jsii.member(jsii_name="sqsQueue")
    def sqs_queue(self) -> aws_cdk.aws_sqs.IQueue:
        """The SQS queue that the worker service will process from."""
        return jsii.get(self, "sqsQueue")

    @property
    @jsii.member(jsii_name="logDriver")
    def log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """The AwsLogDriver to use for logging if logging is enabled."""
        return jsii.get(self, "logDriver")


class _QueueWorkerServiceBaseProxy(QueueWorkerServiceBase):
    pass

class Ec2QueueWorkerService(QueueWorkerServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.Ec2QueueWorkerService"):
    """Class to create an Ec2 query worker service."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mi_b: typing.Optional[jsii.Number]=None, memory_reservation_mi_b: typing.Optional[jsii.Number]=None, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
            memoryLimitMiB: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
            memoryReservationMiB: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
            cluster: Cluster where service will be deployed.
            image: The image to start.
            command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
            desiredTaskCount: Number of desired copies of running tasks. Default: 1
            enableLogging: Flag to indicate whether to enable logging. Default: true
            environment: The environment variables to pass to the container. Default: 'QUEUE_NAME: queue.queueName'
            maxScalingCapacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
            queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. Default: 'SQSQueue with CloudFormation-generated name'
            scalingSteps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        """
        props: Ec2QueueWorkerServiceProps = {"cluster": cluster, "image": image}

        if cpu is not None:
            props["cpu"] = cpu

        if memory_limit_mi_b is not None:
            props["memoryLimitMiB"] = memory_limit_mi_b

        if memory_reservation_mi_b is not None:
            props["memoryReservationMiB"] = memory_reservation_mi_b

        if command is not None:
            props["command"] = command

        if desired_task_count is not None:
            props["desiredTaskCount"] = desired_task_count

        if enable_logging is not None:
            props["enableLogging"] = enable_logging

        if environment is not None:
            props["environment"] = environment

        if max_scaling_capacity is not None:
            props["maxScalingCapacity"] = max_scaling_capacity

        if queue is not None:
            props["queue"] = queue

        if scaling_steps is not None:
            props["scalingSteps"] = scaling_steps

        jsii.create(Ec2QueueWorkerService, self, [scope, id, props])


class FargateQueueWorkerService(QueueWorkerServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.FargateQueueWorkerService"):
    """Class to create a Fargate query worker service."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cpu: typing.Optional[str]=None, memory_mi_b: typing.Optional[str]=None, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments. This default is set in the underlying FargateTaskDefinition construct. Default: 256
            memoryMiB: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU) 1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU) 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU) Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU) Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
            cluster: Cluster where service will be deployed.
            image: The image to start.
            command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
            desiredTaskCount: Number of desired copies of running tasks. Default: 1
            enableLogging: Flag to indicate whether to enable logging. Default: true
            environment: The environment variables to pass to the container. Default: 'QUEUE_NAME: queue.queueName'
            maxScalingCapacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
            queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. Default: 'SQSQueue with CloudFormation-generated name'
            scalingSteps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        """
        props: FargateQueueWorkerServiceProps = {"cluster": cluster, "image": image}

        if cpu is not None:
            props["cpu"] = cpu

        if memory_mi_b is not None:
            props["memoryMiB"] = memory_mi_b

        if command is not None:
            props["command"] = command

        if desired_task_count is not None:
            props["desiredTaskCount"] = desired_task_count

        if enable_logging is not None:
            props["enableLogging"] = enable_logging

        if environment is not None:
            props["environment"] = environment

        if max_scaling_capacity is not None:
            props["maxScalingCapacity"] = max_scaling_capacity

        if queue is not None:
            props["queue"] = queue

        if scaling_steps is not None:
            props["scalingSteps"] = scaling_steps

        jsii.create(FargateQueueWorkerService, self, [scope, id, props])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _QueueWorkerServiceBaseProps(jsii.compat.TypedDict, total=False):
    command: typing.List[str]
    """The CMD value to pass to the container.

    A string with commands delimited by commas.

    Default:
        none
    """
    desiredTaskCount: jsii.Number
    """Number of desired copies of running tasks.

    Default:
        1
    """
    enableLogging: bool
    """Flag to indicate whether to enable logging.

    Default:
        true
    """
    environment: typing.Mapping[str,str]
    """The environment variables to pass to the container.

    Default:
        'QUEUE_NAME: queue.queueName'
    """
    maxScalingCapacity: jsii.Number
    """Maximum capacity to scale to.

    Default:
        (desiredTaskCount * 2)
    """
    queue: aws_cdk.aws_sqs.IQueue
    """A queue for which to process items from.

    If specified and this is a FIFO queue, the queue name must end in the string '.fifo'.

    Default:
        'SQSQueue with CloudFormation-generated name'

    See:
        https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html
    """
    scalingSteps: typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]
    """The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric.

    Maps a range of metric values to a particular scaling behavior.
    https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html

    Default:
        [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.QueueWorkerServiceBaseProps", jsii_struct_bases=[_QueueWorkerServiceBaseProps])
class QueueWorkerServiceBaseProps(_QueueWorkerServiceBaseProps):
    """Properties to define a Query Worker service."""
    cluster: aws_cdk.aws_ecs.ICluster
    """Cluster where service will be deployed."""

    image: aws_cdk.aws_ecs.ContainerImage
    """The image to start."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.Ec2QueueWorkerServiceProps", jsii_struct_bases=[QueueWorkerServiceBaseProps])
class Ec2QueueWorkerServiceProps(QueueWorkerServiceBaseProps, jsii.compat.TypedDict, total=False):
    """Properties to define an Ec2 query worker service."""
    cpu: jsii.Number
    """The minimum number of CPU units to reserve for the container.

    Default:
        - No minimum CPU units reserved.
    """

    memoryLimitMiB: jsii.Number
    """The hard limit (in MiB) of memory to present to the container.

    If your container attempts to exceed the allocated memory, the container
    is terminated.

    At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

    Default:
        - No memory limit.
    """

    memoryReservationMiB: jsii.Number
    """The soft limit (in MiB) of memory to reserve for the container.

    When system memory is under contention, Docker attempts to keep the
    container memory within the limit. If the container requires more memory,
    it can consume up to the value specified by the Memory property or all of
    the available memory on the container instance—whichever comes first.

    At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

    Default:
        - No memory reserved.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.FargateQueueWorkerServiceProps", jsii_struct_bases=[QueueWorkerServiceBaseProps])
class FargateQueueWorkerServiceProps(QueueWorkerServiceBaseProps, jsii.compat.TypedDict, total=False):
    """Properties to define a Fargate queue worker service."""
    cpu: str
    """The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments.

    This default is set in the underlying FargateTaskDefinition construct.

    Default:
        256
    """

    memoryMiB: str
    """The amount (in MiB) of memory used by the task.

    This field is required and you must use one of the following values, which determines your range of valid values
    for the cpu parameter:

    0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU)

    1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU)

    2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU)

    Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU)

    Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU)

    This default is set in the underlying FargateTaskDefinition construct.

    Default:
        512
    """

class ScheduledEc2Task(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledEc2Task"):
    """A scheduled Ec2 task that will be initiated off of cloudwatch events."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, schedule_expression: str, command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, desired_task_count: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, memory_limit_mi_b: typing.Optional[jsii.Number]=None, memory_reservation_mi_b: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            cluster: The cluster where your service will be deployed.
            image: The image to start.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
            cpu: The minimum number of CPU units to reserve for the container. Default: none
            desiredTaskCount: Number of desired copies of running tasks. Default: 1
            environment: The environment variables to pass to the container. Default: none
            memoryLimitMiB: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
            memoryReservationMiB: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        """
        props: ScheduledEc2TaskProps = {"cluster": cluster, "image": image, "scheduleExpression": schedule_expression}

        if command is not None:
            props["command"] = command

        if cpu is not None:
            props["cpu"] = cpu

        if desired_task_count is not None:
            props["desiredTaskCount"] = desired_task_count

        if environment is not None:
            props["environment"] = environment

        if memory_limit_mi_b is not None:
            props["memoryLimitMiB"] = memory_limit_mi_b

        if memory_reservation_mi_b is not None:
            props["memoryReservationMiB"] = memory_reservation_mi_b

        jsii.create(ScheduledEc2Task, self, [scope, id, props])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _ScheduledEc2TaskProps(jsii.compat.TypedDict, total=False):
    command: typing.List[str]
    """The CMD value to pass to the container.

    A string with commands delimited by commas.

    Default:
        none
    """
    cpu: jsii.Number
    """The minimum number of CPU units to reserve for the container.

    Default:
        none
    """
    desiredTaskCount: jsii.Number
    """Number of desired copies of running tasks.

    Default:
        1
    """
    environment: typing.Mapping[str,str]
    """The environment variables to pass to the container.

    Default:
        none
    """
    memoryLimitMiB: jsii.Number
    """The hard limit (in MiB) of memory to present to the container.

    If your container attempts to exceed the allocated memory, the container
    is terminated.

    At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

    Default:
        - No memory limit.
    """
    memoryReservationMiB: jsii.Number
    """The soft limit (in MiB) of memory to reserve for the container.

    When system memory is under contention, Docker attempts to keep the
    container memory within the limit. If the container requires more memory,
    it can consume up to the value specified by the Memory property or all of
    the available memory on the container instance—whichever comes first.

    At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

    Default:
        - No memory reserved.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledEc2TaskProps", jsii_struct_bases=[_ScheduledEc2TaskProps])
class ScheduledEc2TaskProps(_ScheduledEc2TaskProps):
    cluster: aws_cdk.aws_ecs.ICluster
    """The cluster where your service will be deployed."""

    image: aws_cdk.aws_ecs.ContainerImage
    """The image to start."""

    scheduleExpression: str
    """The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

    For more information, see Schedule Expression Syntax for
    Rules in the Amazon CloudWatch User Guide.

    See:
        http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
    """

__all__ = ["Ec2QueueWorkerService", "Ec2QueueWorkerServiceProps", "FargateQueueWorkerService", "FargateQueueWorkerServiceProps", "LoadBalancedEc2Service", "LoadBalancedEc2ServiceProps", "LoadBalancedFargateService", "LoadBalancedFargateServiceApplet", "LoadBalancedFargateServiceAppletProps", "LoadBalancedFargateServiceProps", "LoadBalancedServiceBase", "LoadBalancedServiceBaseProps", "LoadBalancerType", "QueueWorkerServiceBase", "QueueWorkerServiceBaseProps", "ScheduledEc2Task", "ScheduledEc2TaskProps", "__jsii_assembly__"]

publication.publish()
