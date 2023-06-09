
from dataset.basedataset import BaseRGBTDataet
from utils import *
import os
from metrics import MPR,MSR

class GTOT(BaseRGBTDataet):
    """
    Publication: `Learning collaborative sparse representation for grayscale-thermal tracking` 2016\\
    IEEE Transactions on Image Processing \\
    [Download Dataset.](https://github.com/mmic-lcl/Datasets-and-benchmark-code)

    NOTE: this is not support attribute test. [Just here, not GTOT]
    """
    def __init__(self, gt_path="./gt_file/GTOT/groundtruth/",
                 seq_name_path="./gt_file/GTOT/SequencesName.txt") -> None:
        seqs = load_text(seq_name_path, dtype=str)
        super().__init__(gt_path=gt_path, seqs=seqs, bbox_type='ltrb', v_name='groundTruth_v.txt', i_name='groundTruth_i.txt')
        # super().__init__(gt_path=gt_path, seqs=seqs, bbox_type='ltwh', v_name='init.txt', i_name='init.txt')

        self.name = 'GTOT'
        self.MPR_fun = MPR(thr=np.linspace(0, 25, 51))
        self.MSR_fun = MSR(thr=np.linspace(0, 1, 51))

        # Challenge attributes
        self._attr_list = (None)

    def get_attr_list(self):
        return self._attr_list

    def choose_serial_by_att(self, attr):
        return None

    def MPR(self, tracker_name=None, seqs=None):
        """
        Parameters
        ----------
        [in] tracker_name - str
            Default is None, evaluate all registered trackers.
        [in] seqs - list
            Sequence to be evaluated, default is all.
        
        Returns
        -------
        [out0] When evaluating a single tracker, return MPR and the precision Rate at different thresholds.
        [out1] Other cases return a dictionary with all tracker results.
        """
        if seqs==None:
            seqs = self.seqs_name

        if tracker_name!=None:
            return self.MPR_fun(self, self.trackers[tracker_name], seqs)
        else:
            res = {}
            for k,v in self.trackers.items():
                res[k] = list(self.MPR_fun(self, v, seqs))
                res[k][0] = res[k][1].mean(axis=0)[10]
            return res


    def MSR(self, tracker_name=None, seqs=None):
        """
        NOTE
        ---------
        > Maximum Success Rate (MSR). SR is the ratio of the number of successful frames whose 
        overlap is larger than a threshold. Similar to MPR, we also define maximum success 
        rate (MSR) to measure the tracker results. By varying the threshold, the MSR plot can 
        be obtained, and we employ the area under curve of MSR plot to define the representative MSR.

        Parameters
        ----------
        [in] tracker_name - str
            Default is None, evaluate all registered trackers.
        [in] seqs - list
            Sequence to be evaluated, default is all.
        
        Returns
        -------
        Same as MPR.
        """
        if seqs==None:
            seqs = self.seqs_name

        if tracker_name!=None:
            return self.MSR_fun(self, self.trackers[tracker_name], seqs)
        else:
            res = {}
            for k,v in self.trackers.items():
                res[k] = self.MSR_fun(self, v, seqs)
            return res

    def draw_plot(self, metric_fun, filename=None, title=None, seqs=None):
        assert metric_fun==self.MSR or metric_fun==self.MPR
        if filename==None:
            filename = self.name
            if metric_fun==self.MPR:
                filename+="_MPR"
                axis = self.MPR_fun.thr
                loc = "lower right"
            elif metric_fun==self.MSR:
                filename+="_MSR"
                axis = self.MSR_fun.thr
                loc = "lower left"
            filename+="_plot.png"

        if title==None:
            if metric_fun==self.MPR:
                title="Precision Plot"
            elif metric_fun==self.MSR:
                title="Success Plot"

        return super().draw_plot(axis=axis, 
                                 metric_fun=metric_fun, 
                                 filename=filename, 
                                 title=title, 
                                 seqs=seqs, y_max=1.0, y_min=0.0, loc=loc)