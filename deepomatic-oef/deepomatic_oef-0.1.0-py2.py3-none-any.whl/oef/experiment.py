from deepomatic.oef.utils import serializer
from deepomatic.oef.protos import experiment_pb2

class Experiment(serializer.Serializer):
    """An experiment object

    Keyword arguments:
    dataset -- the dataset used to train or evaluate
    """

serializer.register_all(__name__, experiment_pb2)
