
from dataset.basedataset import BaseRGBTDataet
from utils import *
import os
from metrics import PR,SR

class LasHeR(BaseRGBTDataet):
    """
    
    """
    def __init__(self, gt_path='./gt_file/LasHeR/lasher_gt/',
                 seq_name_path="./gt_file/LasHeR/lashertest.txt") -> None:
        seqs = load_text(seq_name_path, dtype=str)
        super().__init__(gt_path=gt_path, seqs=seqs, bbox_type='ltwh')

        self.name = 'LasHeR_test'
        self.PR_fun = PR()
        self.SR_fun = SR()
        self.NPR_fun = None

        # Challenge attributes
        self._attr_list = ('NO', 'PO', 'TO', 'HO', 'MB', 
                           'LI', 'HI', 'AIV', 'LR', 'DEF', 
                           'BC', 'SA', 'CM', 'TC', 'FL', 
                           'OV', 'FM', 'SV', 'ARC')
        self.NO = self.choose_serial_by_att('NO')
        self.PO = self.choose_serial_by_att('PO')
        self.TO = self.choose_serial_by_att('TO')
        self.HO = self.choose_serial_by_att('HO')
        self.MB = self.choose_serial_by_att('MB')
        self.LI = self.choose_serial_by_att('LI')
        self.HI = self.choose_serial_by_att('HI')
        self.AIV = self.choose_serial_by_att('AIV')
        self.LR = self.choose_serial_by_att('LR')
        self.DEF = self.choose_serial_by_att('DEF')
        self.BC = self.choose_serial_by_att('BC')
        self.SA = self.choose_serial_by_att('SA')
        self.CM = self.choose_serial_by_att('CM')
        self.TC = self.choose_serial_by_att('TC')
        self.FL = self.choose_serial_by_att('FL')
        self.OV = self.choose_serial_by_att('OV')
        self.FM = self.choose_serial_by_att('FM')
        self.SV = self.choose_serial_by_att('SV')
        self.ARC = self.choose_serial_by_att('ARC')

    def get_attr_list(self):
        return self._attr_list

    def choose_serial_by_att(self, attr):
        if attr==self.ALL:
            return self.seqs_name
        else:
            seqs = []
            for seq in self.seqs_name:
                i = self.get_attr_list().index(attr)
                path = os.path.join('./gt_file/LasHeR/AttriSeqsTxt', seq+'.txt')
                p = load_text(path)[i]
                if p==1.:
                    seqs.append(seq)
            return seqs

    def PR(self, tracker_name=None, seqs=None):
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
            return self.PR_fun(self, self.trackers[tracker_name], seqs)
        else:
            res = {}
            for k,v in self.trackers.items():
                res[k] = self.PR_fun(self, v, seqs)
            return res


    def SR(self, tracker_name=None, seqs=None):
        """
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
            return self.SR_fun(self, self.trackers[tracker_name], seqs)
        else:
            res = {}
            for k,v in self.trackers.items():
                res[k] = self.SR_fun(self, v, seqs)
            return res


    def draw_attributeRadar(self, metric_fun, filename=None):
        if filename==None:
            filename = self.name
            if metric_fun==self.PR:
                filename+="_PR"
            elif metric_fun==self.SR:
                filename+="_SR"
            filename+="_radar.png"
        return super().draw_attributeRadar(metric_fun, filename)
    

    def draw_plot(self, metric_fun, filename=None, title=None, seqs=None):
        assert metric_fun==self.SR or metric_fun==self.PR
        if filename==None:
            filename = self.name
            if metric_fun==self.PR:
                filename+="_PR"
                axis = self.PR_fun.thr
                loc = "lower right"
            elif metric_fun==self.SR:
                filename+="_SR"
                axis = self.SR_fun.thr
                loc = "lower left"
            filename+="_plot.png"

        if title==None:
            if metric_fun==self.PR:
                title="Precision Plot"
            elif metric_fun==self.SR:
                title="Success Plot"

        return super().draw_plot(axis=axis, 
                                 metric_fun=metric_fun, 
                                 filename=filename, 
                                 title=title, 
                                 seqs=seqs, y_max=1.0, y_min=0.0, loc=loc)