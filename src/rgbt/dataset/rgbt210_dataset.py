
from .basedataset import BaseRGBTDataet,_basepath
from rgbt.utils import *
import os
from rgbt.metrics import PR,SR

class RGBT210(BaseRGBTDataet):
    """
    RGBT210 dataset is the subset of RGBT234.\r
    `Weighted Sparse Representation Regularized Graph Learning for RGB-T Object Tracking.`\r
    [Paper](https://dl.acm.org/doi/pdf/10.1145/3123266.3123289) \r
    [Download Dataset.](https://github.com/mmic-lcl/Datasets-and-benchmark-code)
    """
    def __init__(self, gt_path=f'{_basepath}/gt_file/RGBT210/groundtruth/',
                 seq_name_path=f"{_basepath}/gt_file/RGBT210/SequencesName.txt") -> None:
        seqs = load_text(seq_name_path, dtype=str)
        super().__init__(gt_path=gt_path, seqs=seqs, bbox_type='ltwh', v_name='init.txt', i_name='init.txt')

        self.name = 'RGBT210'
        self.PR_fun = PR()
        self.SR_fun = SR()

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

    def __call__(self, tracker_name, result_path: str, seqs=None, prefix='', bbox_type='ltwh'):
        RGBT_start()
        res = super().__call__(tracker_name, result_path, seqs, prefix, bbox_type)
        RGBT_end()
        return res

    def get_attr_list(self):
        return self._attr_list

    def choose_serial_by_att(self, attr):
        if attr==self.ALL:
            return self.seqs_name
        else:
            p = load_text(os.path.join(self.gt_path, '..', 'attr_txt', attr+'.txt'))
            with open(os.path.join(self.gt_path, '..', 'attr_txt', 'SequencesName.txt')) as f:
                seq_name_s = f.read().split('\n')
            seq_name_s = seq_name_s[:len(p)]
            return [seq_name for i,seq_name in zip(p, seq_name_s) if (i and seq_name in self.seqs_name)]



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
        [out0] When evaluating a single tracker, return PR and the precision Rate at different thresholds.
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
        [out0] When evaluating a single tracker, return SR and the Success Rate at different thresholds.
        [out1] Other cases return a dictionary with all tracker results.
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
                x_label = "Location error threshold"
                y_label = "Precision"
            elif metric_fun==self.SR:
                filename+="_SR"
                axis = self.SR_fun.thr
                loc = "lower left"
                x_label = "overlap threshold"
                y_label = "Success Rate"
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
                                 seqs=seqs, y_max=1.0, y_min=0.0, loc=loc,
                                 x_label=x_label, y_label=y_label)