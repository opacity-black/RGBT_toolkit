
from rgbt.utils import Array
from .base import Metric
from rgbt.dataset.basedataset import BaseRGBTDataet, TrackerResult
import numpy as np

from rgbt.utils import *


class MPR(Metric):
    """
    NOTE
    ---------
    Maximum Precision Rate (MPR). PR is the percentage of frames whose output location 
    is within the given threshold distance of ground truth. That is to say, it computes 
    the average Euclidean distance between the center locations of the tracked target 
    and the manually labeled ground-truth positions of all the frames. Although our 
    alignment between two modalities is highly accurate, there still exist small alignment 
    errors. Therefore, we use maximum precision rate (MPR) instead of PR in this paper. 
    Specifically, for each frame, we compute the above Euclidean distance on both RGB and 
    thermal modalities, and adopt the smaller distance to compute the precision. 
    We set the threshold to be 20 pixels to obtain the representative MPR.
    """
    def __init__(self, thr=np.linspace(0, 50, 51)) -> None:
        super().__init__()
        self.thr = thr

    def seq_worker(self, gtBoxV_li:list, gtBoxI_li:list, predBox_li:list) -> Array:
        get_mpr = lambda pred,gt_v,gt_i : min(CLE(pred, gt_v), CLE(pred, gt_i))
        frame_pr_li = np.array(list(map(get_mpr, predBox_li, gtBoxV_li, gtBoxI_li)))

        seq_length = len(frame_pr_li)
        seq_pr_curve = np.array([np.sum(frame_pr_li<=i)/seq_length for i in self.thr])
        return seq_pr_curve

    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list) -> tuple[float, Array]:
        seq_pr_curve_li = super().process(dataset, result, seqs)
        pr = seq_pr_curve_li.mean(axis=0)[20]
        return pr, seq_pr_curve_li



class MSR(Metric):
    """
    NOTE
    ---------
    Maximum Success Rate (MSR). SR is the ratio of the number of successful frames whose 
    overlap is larger than a threshold. Similar to MPR, we also define maximum success 
    rate (MSR) to measure the tracker results. By varying the threshold, the MSR plot can 
    be obtained, and we employ the area under curve of MSR plot to define the representative MSR.
    """
    def __init__(self, thr=np.linspace(0, 1, 21)) -> None:
        super().__init__()
        self.thr = thr


    def seq_worker(self, gtBoxV_li:list, gtBoxI_li:list, predBox_li:list) -> Array:
        get_msr = lambda pred,gt_v,gt_i : max(IoU(pred, gt_v), IoU(pred, gt_i))
        frame_sr_li = np.array(list(map(get_msr, predBox_li, gtBoxV_li, gtBoxI_li)))

        seq_length = len(frame_sr_li)
        seq_sr_curve = np.array([np.sum(frame_sr_li>i)/seq_length for i in self.thr])
        return seq_sr_curve

    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list) -> tuple[float, Array]:
        seq_sr_curve_li = super().process(dataset, result, seqs)
        sr = seq_sr_curve_li.mean()
        return sr, seq_sr_curve_li



class MPR_GTOT(Metric):
    """
    NOTE
    ---------
    Maximum Precision Rate (MPR). PR is the percentage of frames whose output location 
    is within the given threshold distance of ground truth. That is to say, it computes 
    the average Euclidean distance between the center locations of the tracked target 
    and the manually labeled ground-truth positions of all the frames. Although our 
    alignment between two modalities is highly accurate, there still exist small alignment 
    errors. Therefore, we use maximum precision rate (MPR) instead of PR in this paper. 
    Specifically, for each frame, we compute the above Euclidean distance on both RGB and 
    thermal modalities, and adopt the smaller distance to compute the precision. 
    We set the threshold to be 20 pixels to obtain the representative MPR.
    """
    def __init__(self, thr=np.linspace(0, 25, 51)) -> None:
        super().__init__()
        self.thr = thr

    def seq_worker(self, gtBoxV_li:list, gtBoxI_li:list, predBox_li:list) -> Array:
        get_mpr = lambda pred,gt_v,gt_i : min(CLE(pred, gt_v), CLE(pred, gt_i))
        frame_pr_li = np.array(list(map(get_mpr, predBox_li, gtBoxV_li, gtBoxI_li)))
        seq_pr_curve = np.array([np.sum(frame_pr_li<=i) for i in self.thr])
        return seq_pr_curve

    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list) -> tuple[float, Array]:
        all_frame_num = sum([len(dataset[seq]['visible']) for seq in seqs])
        seq_pr_curve_li = super().process(dataset, result, seqs)
        pr = seq_pr_curve_li[:, 10].sum()/all_frame_num
        return pr, seq_pr_curve_li/all_frame_num*seq_pr_curve_li.shape[0]



class MSR_GTOT(Metric):
    """
    NOTE
    ---------
    Maximum Success Rate (MSR). SR is the ratio of the number of successful frames whose 
    overlap is larger than a threshold. Similar to MPR, we also define maximum success 
    rate (MSR) to measure the tracker results. By varying the threshold, the MSR plot can 
    be obtained, and we employ the area under curve of MSR plot to define the representative MSR.
    """
    def __init__(self, thr=np.linspace(0, 1, 21)) -> None:
        super().__init__()
        self.thr = thr

    def seq_worker(self, gtBoxV_li:list, gtBoxI_li:list, predBox_li:list) -> Array:
        get_msr = lambda pred,gt_v,gt_i : max(IoU(pred, gt_v), IoU(pred, gt_i))
        frame_sr_li = np.array(list(map(get_msr, predBox_li, gtBoxV_li, gtBoxI_li)))

        seq_sr_curve = np.array([np.sum(frame_sr_li>i) for i in self.thr])
        return seq_sr_curve


    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list) -> tuple[float, Array]:
        all_frame_num = sum([len(dataset[seq]['visible']) for seq in seqs])
        seq_sr_curve_li = super().process(dataset, result, seqs)
        
        a = (seq_sr_curve_li[:, 1:]*self.thr[1]).sum()   # calc auc
        b = (seq_sr_curve_li[:, :-1]*self.thr[1]).sum()
        sr_val = (a+b)/2./all_frame_num
        return sr_val, seq_sr_curve_li/all_frame_num*seq_sr_curve_li.shape[0]



class PR(Metric):
    """
    Precision Rate.
    """
    def __init__(self, thr=np.linspace(0, 50, 51)) -> None:
        super().__init__()
        self.thr = thr

    def seq_worker(self, predBox_li, gtBoxV_li) -> Array:
        predBox_li[0] = gtBoxV_li[0]
        frame_pr_li = np.array(list(map(CLE, predBox_li, gtBoxV_li)))

        seq_length = len(frame_pr_li)
        seq_pr_curve = np.array([np.sum(frame_pr_li<=i)/seq_length for i in self.thr])
        return seq_pr_curve

    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list) -> tuple[float, Array]:
        seq_pr_curve_li = super().process(dataset, result, seqs, mm='visible' in dataset[0])
        pr = seq_pr_curve_li.mean(axis=0)[20]
        return pr, seq_pr_curve_li





class SR(Metric):
    """
    Success Rate.
    """
    def __init__(self, thr=np.linspace(0, 1, 21)) -> None:
        super().__init__()
        self.thr = thr


    def seq_worker(self, predBox_li, gtBoxV_li) -> Array:
        predBox_li[0] = gtBoxV_li[0]
        frame_sr_li = np.array(list(map(IoU, predBox_li, gtBoxV_li)))

        seq_length = len(frame_sr_li)
        seq_sr_curve = np.array([np.sum(frame_sr_li>i)/seq_length for i in self.thr])
        return seq_sr_curve

    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list) -> tuple[float, Array]:
        seq_sr_curve_li = super().process(dataset, result, seqs, mm='visible' in dataset[0])
        sr = seq_sr_curve_li.mean()
        return sr, seq_sr_curve_li


class SR_LasHeR(Metric):
    """
    Success Rate for LasHeR.
    """
    def __init__(self, thr=np.linspace(0, 1, 21)) -> None:
        super().__init__()
        self.thr = thr

    def seq_worker(self, predBox_li, gtBoxV_li) -> Array:
        assert len(predBox_li)>=len(gtBoxV_li)
        seq_length = len(gtBoxV_li)
        # ignore the first frame
        predBox_li[0] = gtBoxV_li[0]
        # cut off tracking result
        predBox_li = predBox_li[:seq_length]
        # handle the invailded tracking result
        for i in range(1, seq_length):
            if predBox_li[i][2]<=0 or predBox_li[i][3]<=0:
                predBox_li[i] = predBox_li[i-1].copy()
        frame_sr_li = np.array(list(map(IoU, predBox_li, gtBoxV_li)))

        for i in range(seq_length):
            if sum(gtBoxV_li[i]<=0):
                frame_sr_li[i]=-1

        seq_sr_curve = np.array([np.sum(frame_sr_li>i)/seq_length for i in self.thr])
        return seq_sr_curve


    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list) -> tuple[float, Array]:
        seq_sr_curve_li = super().process(dataset, result, seqs, mm='visible' in dataset[0])
        sr = seq_sr_curve_li.mean()
        return sr, seq_sr_curve_li
    

class PR_LasHeR(Metric):
    """
    Precision Rate.
    Different other dataset, LasHeR testingset need to filter some results.
    """
    def __init__(self, thr=np.linspace(0, 50, 51)) -> None:
        super().__init__()
        self.thr = thr

    def seq_worker(self, predBox_li, gtBoxV_li) -> Array:
        assert len(predBox_li)>=len(gtBoxV_li)
        seq_length = len(gtBoxV_li)
        # ignore the first frame
        predBox_li[0] = gtBoxV_li[0]
        # cut off tracking result
        predBox_li = predBox_li[:seq_length]
        # handle the invailded tracking result
        for i in range(1, seq_length):
            if predBox_li[i][2]<=0 or predBox_li[i][3]<=0:
                predBox_li[i] = predBox_li[i-1].copy()
        frame_pr_li = np.array(list(map(CLE, predBox_li, gtBoxV_li)))

        for i in range(seq_length):
            if sum(gtBoxV_li[i]<=0):
                frame_pr_li[i]=-1

        seq_pr_curve = np.array([np.sum(frame_pr_li<=i)/seq_length for i in self.thr])
        return seq_pr_curve


    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list) -> tuple[float, Array]:
        seq_pr_curve_li = super().process(dataset, result, seqs, mm='visible' in dataset[0])
        pr = seq_pr_curve_li.mean(axis=0)[20]
        return pr, seq_pr_curve_li


class NPR(Metric):
    """
    Normalized Precision Rate.
    """
    def __init__(self, thr=np.linspace(0, 0.5, 51)) -> None:
        super().__init__()
        self.thr = thr

    def seq_worker(self, predBox_li, gtBoxV_li) -> Array:
        assert len(predBox_li)>=len(gtBoxV_li)
        seq_length = len(gtBoxV_li)
        # ignore the first frame
        predBox_li[0] = gtBoxV_li[0]
        # cut off tracking result
        predBox_li = predBox_li[:seq_length]
        # handle the invailded tracking result
        for i in range(1, seq_length):
            if predBox_li[i][2]<=0 or predBox_li[i][3]<=0:
                predBox_li[i] = predBox_li[i-1].copy()
        frame_npr_li = np.array(list(map(normalize_CLE, predBox_li, gtBoxV_li)))

        for i in range(seq_length):
            if sum(gtBoxV_li[i]<=0):
                frame_npr_li[i]=-1

        seq_npr_curve = np.array([np.sum(frame_npr_li<=i)/seq_length for i in self.thr])
        return seq_npr_curve


    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list):
        seq_npr_curve_li = super().process(dataset, result, seqs, mm='visible' in dataset[0])
        npr = seq_npr_curve_li.mean(axis=0)[20]
        return npr, seq_npr_curve_li

