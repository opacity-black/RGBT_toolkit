
from .basedataset import BaseRGBTDataet,_basepath
from rgbt.utils import *
import os
from rgbt.metrics import PR_LasHeR,SR_LasHeR,NPR
from rgbt.vis.default_config import Setting, get_PR_Setting, get_SR_Setting

class LasHeR(BaseRGBTDataet):
    """
    Publication: `LasHeR: A Large-scale High-diversity Benchmark for RGBT Tracking`
    [Download Dataset.](https://github.com/mmic-lcl/Datasets-and-benchmark-code)
    """
    def __init__(self, gt_path=f'{_basepath}/gt_file/LasHeR/lasher_gt/',
                 seq_name_path=f"{_basepath}/gt_file/LasHeR/lashertest.txt") -> None:
        seqs = load_text(seq_name_path, dtype=str)
        super().__init__(gt_path=gt_path, seqs=seqs, bbox_type='ltwh')

        self.name = 'LasHeR_test'
        self.PR_fun = PR_LasHeR()
        self.SR_fun = SR_LasHeR()
        self.NPR_fun = NPR()

        
        self.PR_PlotSetting = get_PR_Setting()
        self.PR_PlotSetting.axis = self.PR_fun.thr
        self.PR_PlotSetting.filename = self.name+"_PR_plot.png"
        self.PR_PlotSetting.title = "Precision plots of OPE on LasHeR"
        
        self.SR_PlotSetting = get_SR_Setting()
        self.SR_PlotSetting.axis = self.SR_fun.thr
        self.SR_PlotSetting.filename = self.name+"_SR_plot.png"
        self.SR_PlotSetting.title = "Success plots of OPE on LasHeR"

        self.NPR_PlotSetting = get_PR_Setting()
        self.NPR_PlotSetting.axis = self.NPR_fun.thr
        self.NPR_PlotSetting.filename = self.name+"_NPR_plot.png"
        self.NPR_PlotSetting.legend_loc = "lower right"
        self.NPR_PlotSetting.xlabel = "Normalized Location error threshold"
        self.NPR_PlotSetting.ylabel = "Normalized Precision"
        self.NPR_PlotSetting.title="Normalized Precision plots of OPE on LasHeR"


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
                path = os.path.join(self.gt_path, '..', 'AttriSeqsTxt', seq+'.txt')
                p = load_text(path)[i]
                if p==1.:
                    seqs.append(seq)
            return seqs

    def PR(self, tracker_name:Any=None, seqs=None):
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

    def NPR(self, tracker_name:Any=None, seqs=None):
        """
        """
        if seqs==None:
            seqs = self.seqs_name

        if tracker_name!=None:
            return self.NPR_fun(self, self.trackers[tracker_name], seqs)
        else:
            res = {}
            for k,v in self.trackers.items():
                res[k] = self.NPR_fun(self, v, seqs)
            return res


    def SR(self, tracker_name:Any=None, seqs=None):
        """
        Parameters
        ----------
        [in] tracker_name - str
            Default is None, evaluate all registered trackers.
        [in] seqs - list
            Sequence to be evaluated, default is all.
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
    

    def pr_plot(self, filename=None, seqs=None, plotSetting=None):
        metric_fun=self.PR
        if filename!=None:
            self.PR_PlotSetting.filename = filename
        if plotSetting==None:
            plotSetting = self.PR_PlotSetting
        return super().plot(metric_fun=metric_fun, seqs=seqs, plotSetting=plotSetting)
    
    def npr_plot(self, filename=None, seqs=None, plotSetting=None):
        metric_fun=self.NPR
        if plotSetting==None:
            plotSetting = self.NPR_PlotSetting
        if filename!=None:
            plotSetting.filename = filename
        return super().plot(metric_fun=metric_fun, seqs=seqs, plotSetting=plotSetting)

    def sr_plot(self, filename=None, seqs=None, plotSetting=None):
        metric_fun=self.SR
        if plotSetting==None:
            plotSetting = self.SR_PlotSetting
        if filename!=None:
            plotSetting.filename = filename
        return super().plot(metric_fun=metric_fun, seqs=seqs, plotSetting=plotSetting)