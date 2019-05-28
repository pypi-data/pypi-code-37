from deepomatic.oef.utils import serializer
from deepomatic.oef.protos import nets_pb2


class NetArchitecture(serializer.Serializer):
    """
    An net architecture

    Keyword arguments:
    type -- for example NetArchitecture.RESNET_V2_101
    """

    arch_to_name = {v: k for k, v in nets_pb2.NetArchitecture.ArchitectureType.items()}
    pretraining_to_name = {v: k for k, v in nets_pb2.NetArchitecture.PretrainingType.items()}

    @classmethod
    def get_arch_name(cls, arch):
        return cls.arch_to_name[arch]

    @classmethod
    def get_pretraining_name(cls, pretraining):
        return cls.pretraining_to_name[pretraining]


serializer.register_all(__name__, nets_pb2)
