
from rgbt.dataset.basedataset import BaseRGBTDataet, TrackerResult


class Metric:
    def __init__(self) -> None:
        pass

    def __call__(self, dataset:BaseRGBTDataet, res:TrackerResult):
        pass


    def __call__(self, dataset:BaseRGBTDataet):
        self(dataset, dataset.trackers)
