try:
    import maskrcnn_benchmark
except ModuleNotFoundError as e:
    print('maskrcnn_benchmark not found. Install maskrcnn_benchmark according https://github.com/facebookresearch/maskrcnn-benchmark')


from maskrcnn_benchmark.modeling.detector import build_detection_model
from maskrcnn_benchmark.config.defaults import _C as default_cfg


def maskrcnn(cfg=None):
    if cfg is None:
        cfg = default_cfg
    return build_detection_model(cfg)
