
from rgbt.dataset.basedataset import BaseRGBTDataet, TrackerResult
from rgbt.utils import Array
import os
from joblib import Parallel, delayed
import numpy as np

class Metric:
    def __init__(self) -> None:
        cpu_count = os.cpu_count()
        self.job_count = 6 if cpu_count!=None and cpu_count>=6 else cpu_count

    def seq_worker(self, ) -> Array:
        raise ImportError

    def process(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list, mm=True) -> Array:
        # 串行
        if len(seqs)<30:
            if mm:
                params = [[dataset[sn]['visible'], dataset[sn]['infrared'], result[sn]] for sn in seqs]
            else:
                params = [[dataset[sn], result[sn]] for sn in seqs]
            seq_curve_li = np.array(list(map(self.seq_worker, *list(zip(*params)))))      # shape: seqs_num, thr_num
        # 并行 效率提升一倍以上
        else:
            if mm:
                seq_curve_li = np.array(Parallel(n_jobs=self.job_count)(delayed(
                    self.seq_worker)(dataset[sn]['visible'], dataset[sn]['infrared'], result[sn]) for sn in seqs))      # shape: seqs_num, thr_num
            else:
                seq_curve_li = np.array(Parallel(n_jobs=self.job_count)(delayed(
                    self.seq_worker)(dataset[sn], result[sn]) for sn in seqs))      # shape: seqs_num, thr_num
        return seq_curve_li

    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list) -> tuple[float, Array]:
            raise ImportError