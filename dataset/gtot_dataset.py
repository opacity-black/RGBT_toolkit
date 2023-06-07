
from dataset.basedataset import BaseRGBTDataet
from utils import *
import os
from metrics import PR,SR

class GTOT(BaseRGBTDataet):
    """
    Publication: `Learning collaborative sparse representation for grayscale-thermal tracking`\r
    IEEE Transactions on Image Processing
    [Download Dataset.](https://github.com/mmic-lcl/Datasets-and-benchmark-code)
    """
    def __init__(self, gt_path,
                 seq_name_path="./gt_file/GTOT/SequencesName.txt") -> None:
        seqs = load_text(seq_name_path, dtype=str)
        super().__init__(gt_path=gt_path, seqs=seqs, bbox_type='ltwh', v_name='groundTruth_v.txt', i_name='groundTruth_i.txt')

        self.name = 'GTOT'
        self.MPR_fun = PR()
        self.MSR_fun = SR()

        # Challenge attributes
        self._attr_list = ("BC","CM","DEF","FM","HO","LI","LR","MB","NO","TC","PO","SC")
        self.BC = self.choose_serial_by_att("BC")
        self.CM = self.choose_serial_by_att("CM")
        self.DEF = self.choose_serial_by_att("DEF")
        self.FM = self.choose_serial_by_att("FM")
        self.HO = self.choose_serial_by_att("HO")
        self.LI = self.choose_serial_by_att("LI")
        self.LR = self.choose_serial_by_att("LR")
        self.MB = self.choose_serial_by_att("MB")
        self.NO = self.choose_serial_by_att("NO")
        self.TC = self.choose_serial_by_att("TC")
        self.PO = self.choose_serial_by_att("PO")
        self.SC = self.choose_serial_by_att("SC")

    def get_attr_list(self):
        return self._attr_list

    def choose_serial_by_att(self, attr):
        if attr==self.ALL:
            return self.seqs_name
        else:
            p = load_text(os.path.join(self.gt_path, '..', 'attr_txt', attr+'.txt'))
            return [seq_name for i,seq_name in zip(p, self.seqs_name) if i]

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
                res[k] = self.MPR_fun(self, v, seqs)
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
