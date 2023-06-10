
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


    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list):
        pr=[]
        for seq_name in seqs:
            gt_v = dataset[seq_name]['visible']
            gt_i = dataset[seq_name]['infrared']
            serial = result[seq_name]
            res_v = np.array(serial_process(CLE, serial, gt_v))
            res_i = np.array(serial_process(CLE, serial, gt_i))
            res = np.minimum(res_v, res_i)

            pr_cell = []
            for i in self.thr:
                pr_cell.append(np.sum(res<=i)/len(res))
            pr.append(pr_cell)
        pr = np.array(pr)
        pr_val = pr.mean(axis=0)[20]
        return pr_val, pr



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


    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list):
    
        sr=[]
        for seq_name in seqs:
            gt_v = dataset[seq_name]['visible']
            gt_i = dataset[seq_name]['infrared']
            serial = result[seq_name]
            res_v = np.array(serial_process(IoU, serial, gt_v))
            res_i = np.array(serial_process(IoU, serial, gt_i))
            res = np.maximum(res_v, res_i)

            sr_cell = []
            for i in self.thr:
                sr_cell.append(np.sum(res>i)/len(res))
            sr.append(sr_cell)

        sr = np.array(sr)
        sr_val = sr.mean()
        return sr_val, sr



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


    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list):
        pr=[]
        all_frame_num = 0
        for seq_name in seqs:
            gt_v = dataset[seq_name]['visible']
            gt_i = dataset[seq_name]['infrared']
            serial = result[seq_name]
            res_v = np.array(serial_process(CLE, serial, gt_v))
            res_i = np.array(serial_process(CLE, serial, gt_i))
            res = np.minimum(res_v, res_i)

            pr_cell = []
            all_frame_num+=len(res)
            for i in self.thr:
                pr_cell.append(np.sum(res<i))
            pr.append(pr_cell)

        pr = np.array(pr)
        pr_val = pr[:, 10].sum()/all_frame_num
        return pr_val, pr/all_frame_num*pr.shape[0]



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


    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list):
    
        sr=[]
        all_frame_num=0
        for seq_name in seqs:
            gt_v = dataset[seq_name]['visible']
            gt_i = dataset[seq_name]['infrared']
            serial = result[seq_name]
            res_v = np.array(serial_process(IoU, serial, gt_v))
            res_i = np.array(serial_process(IoU, serial, gt_i))
            res = np.maximum(res_v, res_i)

            sr_cell = []
            all_frame_num+=len(res)
            for i in self.thr:
                sr_cell.append(np.sum(res>i))
            sr.append(sr_cell)

        sr = np.array(sr)
        sr_val = 0
        a = (sr[:, 1:]*self.thr[1]).sum()   # calc auc
        b = (sr[:, :-1]*self.thr[1]).sum()
        sr_val += (a+b)/2.
        sr_val = sr_val/all_frame_num
        return sr_val, sr/all_frame_num*sr.shape[0]



class PR(Metric):
    """
    Precision Rate.
    """
    def __init__(self, thr=np.linspace(0, 50, 51)) -> None:
        super().__init__()
        self.thr = thr


    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list):
        pr=[]
        for seq_name in seqs:
            try:
                gt = dataset[seq_name]
                serial = result[seq_name]
                serial[0] = gt[0]       # ignore the first frame
            except:
                gt = dataset[seq_name]['visible']
                serial = result[seq_name]
                serial[0] = gt[0]       # ignore the first frame
            res = np.array(serial_process(CLE, serial, gt))

            pr_cell = []
            for i in self.thr:
                pr_cell.append(np.sum(res<=i)/len(res))
            pr.append(pr_cell)
            
        pr = np.array(pr)
        pr_val = pr.mean(axis=0)[20]
        return pr_val, pr





class SR(Metric):
    """
    Success Rate.
    """
    def __init__(self, thr=np.linspace(0, 1, 21)) -> None:
        super().__init__()
        self.thr = thr


    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list):
    
        sr=[]
        for seq_name in seqs:
            try:
                gt = dataset[seq_name]
                serial = result[seq_name]
                serial[0] = gt[0]       # ignore the first frame
            except:
                gt = dataset[seq_name]['visible']
                serial = result[seq_name]
                serial[0] = gt[0]       # ignore the first frame
            res = np.array(serial_process(IoU, serial, gt))

            sr_cell = []
            for i in self.thr:
                sr_cell.append(np.sum(res>i)/len(res))
            sr.append(sr_cell)

        sr = np.array(sr)
        sr_val = sr.mean()
        return sr_val, sr


class SR_LasHeR(Metric):
    """
    Success Rate.
    Different other dataset, LasHeR testingset need to filter some results.
    """
    def __init__(self, thr=np.linspace(0, 1, 21)) -> None:
        super().__init__()
        self.thr = thr


    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list):
    
        sr=[]
        for seq_name in seqs:
            try:
                gt = dataset[seq_name]
                serial = result[seq_name]
                serial[0] = gt[0]       # ignore the first frame
            except:
                gt = dataset[seq_name]['visible']
                serial = result[seq_name]
                serial[0] = gt[0]       # ignore the first frame
            # cut off tracking result
            serial = serial[:len(gt)]   
            # handle the invailded tracking result
            for i in range(1, len(gt)):
                if serial[i][2]<=0 or serial[i][3]<=0:
                    serial[i] = serial[i-1].copy()
            res = np.array(serial_process(IoU, serial, gt))

            for i in range(len(gt)):
                if sum(gt[i]<=0):
                    res[i]=-1

            sr_cell = []
            for i in self.thr:
                sr_cell.append(np.sum(res>i)/len(res))
            sr.append(sr_cell)

        sr = np.array(sr)
        sr_val = sr.mean()
        return sr_val, sr
    

class PR_LasHeR(Metric):
    """
    Precision Rate.
    Different other dataset, LasHeR testingset need to filter some results.
    """
    def __init__(self, thr=np.linspace(0, 50, 51)) -> None:
        super().__init__()
        self.thr = thr


    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list):
        pr=[]
        for seq_name in seqs:
            try:
                gt = dataset[seq_name]
                serial = result[seq_name]
                serial[0] = gt[0]       # ignore the first frame
            except:
                gt = dataset[seq_name]['visible']
                serial = result[seq_name]
                serial[0] = gt[0]       # ignore the first frame
            # cut off tracking result
            serial = serial[:len(gt)]   
            # handle the invailded tracking result
            for i in range(1, len(gt)):
                if serial[i][2]<=0 or serial[i][3]<=0:
                    serial[i] = serial[i-1].copy()
            res = np.array(serial_process(CLE, serial, gt))

            for i in range(len(gt)):
                if sum(gt[i]<=0):
                    res[i]=-1

            pr_cell = []
            for i in self.thr:
                pr_cell.append(np.sum(res<=i)/len(res))
            pr.append(pr_cell)
            
        pr = np.array(pr)
        pr_val = pr.mean(axis=0)[20]
        return pr_val, pr


class NPR(Metric):
    """
    Normalized Precision Rate.
    """
    def __init__(self, thr=np.linspace(0, 0.5, 51)) -> None:
        super().__init__()
        self.thr = thr


    def __call__(self, dataset:BaseRGBTDataet, result:TrackerResult, seqs:list):
        pr=[]
        for seq_name in seqs:
            try:
                gt = dataset[seq_name]
                serial = result[seq_name]
                serial[0] = gt[0]       # ignore the first frame
            except:
                gt = dataset[seq_name]['visible']
                serial = result[seq_name]
                serial[0] = gt[0]       # ignore the first frame
            # cut off tracking result
            serial = serial[:len(gt)]   
            # handle the invailded tracking result
            for i in range(1, len(gt)):
                if serial[i][2]<=0 or serial[i][3]<=0:
                    serial[i] = serial[i-1].copy()
            res = np.array(serial_process(CLE, serial, gt, need_normalize=True))

            for i in range(len(gt)):
                if sum(gt[i]<=0):
                    res[i]=-1

            pr_cell = []
            for i in self.thr:
                pr_cell.append(np.sum(res<=i)/len(res))
            pr.append(pr_cell)
        pr = np.array(pr)
        pr_val = pr.mean(axis=0)[20]
        return pr_val, pr

