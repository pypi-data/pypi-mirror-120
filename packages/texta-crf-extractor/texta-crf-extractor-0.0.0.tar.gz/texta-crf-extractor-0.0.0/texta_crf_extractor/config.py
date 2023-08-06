
from .feature_extraction import DEFAULT_EXTRACTORS, DEFAULT_LAYERS


class CRFConfig:

    def __init__(
        self,
        num_iter=100,
        test_size=0.3,
        verbose=False,
        c1=1.0,
        c2=1.0,
        bias=True,
        window_size=2,
        context_feature_layers=DEFAULT_LAYERS,
        context_feature_extractors=DEFAULT_EXTRACTORS,
        feature_layers=DEFAULT_LAYERS,
        feature_extractors=DEFAULT_EXTRACTORS
    ):
          
        self.test_size = test_size
        self.verbose = verbose

        self.num_iter = num_iter
        self.c1 = c1
        self.c2 = c2

        self.feature_layers = feature_layers
        self.context_feature_layers = context_feature_layers
        self.feature_extractors = feature_extractors
        self.context_feature_extractors = context_feature_extractors
        self.bias = bias
        self.window_size = window_size
