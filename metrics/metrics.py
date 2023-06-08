
from .base import Metric
from dataset.basedataset import BaseRGBTDataet, TrackerResult
import numpy as np

from utils import *


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
            for i in range(len(gt)-1, -1, -1):
                if (gt[i][2]-gt[i][0])<=0 or (gt[i][3]-gt[i][1])<=0:
                    del gt[i]
                    del serial[i]
            res = np.array(serial_process(CLE, serial, gt, need_normalize=True))

            pr_cell = []
            for i in self.thr:
                pr_cell.append(np.sum(res<=i)/len(res))
            pr.append(pr_cell)
        pr = np.array(pr)
        pr_val = pr.mean(axis=0)[20]
        return pr_val, pr





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
            # cut off tracking result
            serial = serial[:len(gt)]   
            # handle the invailded tracking result
            for i in range(len(gt)-1, -1, -1):
                if (gt[i][2]-gt[i][0])<=0 or (gt[i][3]-gt[i][1])<=0:
                    del gt[i]
                    del serial[i]
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
            # cut off tracking result
            serial = serial[:len(gt)]   
            # handle the invailded tracking result
            for i in range(len(gt)-1, -1, -1):
                if (gt[i][2]-gt[i][0])<=0 or (gt[i][3]-gt[i][1])<=0 :
                    del gt[i]
                    del serial[i]
            res = np.array(serial_process(IoU, serial, gt))

            sr_cell = []
            for i in self.thr:
                sr_cell.append(np.sum(res>i)/len(res))
            sr.append(sr_cell)

        sr = np.array(sr)
        sr_val = sr.mean()
        return sr_val, sr

