
from rgbt.dataset.basedataset import BaseRGBTDataet, TrackerResult,_basepath
from rgbt.utils import *
import os
from rgbt.metrics import MPR,MSR
from rgbt.vis.default_config import Setting, get_PR_Setting, get_SR_Setting


class RGBT234(BaseRGBTDataet):
    """
    RGBT234 dataset: `RGB-T Object Tracking: Benchmark and Baseline.`\r
    [Paper.](https://arxiv.org/abs/1805.08982) \r
    [Download Dataset.](https://github.com/mmic-lcl/Datasets-and-benchmark-code)
    """
    def __init__(self, gt_path=f'{_basepath}/gt_file/RGBT234/rgbt234_gt/',
                 seq_name_path=f"{_basepath}/gt_file/RGBT234/attr_txt/SequencesName.txt") -> None:
        seqs = load_text(seq_name_path, dtype=str)
        super().__init__(gt_path=gt_path, seqs=seqs, bbox_type='ltwh', v_name='visible.txt', i_name='infrared.txt')

        self.name = 'RGBT234'

        self.MPR_fun = MPR()
        self.MSR_fun = MSR()

        self.MPR_PlotSetting = get_PR_Setting()
        self.MPR_PlotSetting.axis = self.MPR_fun.thr
        self.MPR_PlotSetting.filename = self.name+"_MPR_plot.png"
        
        self.MSR_PlotSetting = get_SR_Setting()
        self.MSR_PlotSetting.axis = self.MSR_fun.thr
        self.MSR_PlotSetting.filename = self.name+"_MSR_plot.png"

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


    def __repr__(self) -> str:
        return """RGBT234 dataset: `RGB-T Object Tracking: Benchmark and Baseline.`
                [Paper.](https://arxiv.org/abs/1805.08982)
                [Download Dataset.](https://github.com/mmic-lcl/Datasets-and-benchmark-code)"""


    def __call__(self, tracker_name, result_path: str, seqs=None, prefix='', bbox_type='ltwh') -> TrackerResult:
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
            return [seq_name for i,seq_name in zip(p, self.seqs_name) if i]


    def MPR(self, tracker_name:Any=None, seqs=None):
        """
        NOTE
        ---------
        > Maximum Precision Rate (MPR). PR is the percentage of frames whose output location 
        is within the given threshold distance of ground truth. That is to say, it computes 
        the average Euclidean distance between the center locations of the tracked target 
        and the manually labeled ground-truth positions of all the frames. Although our 
        alignment between two modalities is highly accurate, there still exist small alignment 
        errors. Therefore, we use maximum precision rate (MPR) instead of PR in this paper. 
        Specifically, for each frame, we compute the above Euclidean distance on both RGB and 
        thermal modalities, and adopt the smaller distance to compute the precision. 
        We set the threshold to be 20 pixels to obtain the representative MPR.

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


    def MSR(self, tracker_name:Any=None, seqs=None):
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
        [out0] When evaluating a single tracker, return MSR and the Success Rate at different thresholds.
        [out1] Other cases return a dictionary with all tracker results.
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


    def draw_attributeRadar(self, metric_fun, filename:str=''):
        if filename==None:
            filename = self.name
            if metric_fun==self.MPR:
                filename+="_MPR"
            elif metric_fun==self.MSR:
                filename+="_MSR"
            filename+="_radar.png"
        return super().draw_attributeRadar(metric_fun, filename)


    def pr_plot(self, filename=None, seqs=None, plotSetting=None):
        return self.mpr_plot(filename=filename, seqs=seqs, plotSetting=plotSetting)


    def sr_plot(self, filename=None, seqs=None, plotSetting=None):
        return self.msr_plot(filename=filename, seqs=seqs, plotSetting=plotSetting)


    def mpr_plot(self, filename=None, seqs=None, plotSetting=None):
        metric_fun=self.MPR
        if plotSetting==None:
            plotSetting = self.MPR_PlotSetting
        if filename!=None:
            plotSetting.filename = filename
        return super().plot(metric_fun=metric_fun, seqs=seqs, plotSetting=plotSetting)
    

    def msr_plot(self, filename=None, seqs=None, plotSetting=None):
        metric_fun=self.MSR
        if plotSetting==None:
            plotSetting = self.MSR_PlotSetting
        if filename!=None:
            plotSetting.filename = filename
        return super().plot(metric_fun=metric_fun, seqs=seqs, plotSetting=plotSetting)