from deepomatic.oef.utils import model_list
from deepomatic.oef.utils import class_helpers
from deepomatic.oef.utils.serializer import Serializer
from deepomatic.oef.protos.model_pb2 import Model


class InvalidNet(Exception):
    pass


class ModelBuilder(object):
    """
    This class can build a Model protobuf given the pre-determined parameters. You can also pass
    additionnal parameters to override the default arguments. In that purpose, all fields of Model and its
    sub-messages are assumed to have a different name (this assumpition is checked by model_generator).
    """

    _model_list = None

    def __init__(self, model_type_key):
        if self._model_list is None:
            self.load_model_list()
        if model_type_key not in self._model_list:
            raise InvalidNet("Unknown model {}".format(model_type_key))
        self._model_args = self._model_list[model_type_key]

    @classmethod
    def load_model_list(cls):
        # Avoid to load it at the root of the module to avoid nested import loops

        cls._model_list = {}
        for per_dataset_type_models in model_list.model_list.values():
            for pre_pretraining_type_models in per_dataset_type_models.values():
                for key, args in pre_pretraining_type_models.items():
                    assert key not in cls._model_list, "Duplicate model key, this should not happen"
                    cls._model_list[key] = args

    def build(self, **kwargs):
        return self._recursive_build_(Model, self._model_args.args, self._model_args.default_args, kwargs)

    @staticmethod
    def _recursive_build_(protobuf_class, args, default_args, kwargs):
        real_args = {}
        for field in protobuf_class.DESCRIPTOR.fields:
            if field.name in args:
                assert field.name not in kwargs, "You cannot pass arguments that are set by ModelBuilder"
                value = args[field.name]
                if field.message_type is None:
                    # This field is a scalar field, we just assign the value
                    real_args[field.name] = value
                else:
                    # This fields is a protobuf message, we build it recursively
                    real_args[field.name] = ModelBuilder._recursive_build_(class_helpers.load_proto_class_from_protobuf_descriptor(field.message_type), value, default_args, kwargs)
            elif field.name in kwargs:
                value = kwargs[field.name]
                if isinstance(value, Serializer):
                    value = value._msg
                real_args[field.name] = value
            elif field.name in default_args:
                real_args[field.name] = default_args[field.name]
        return protobuf_class(**real_args)
