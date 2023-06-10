
from rgbt.utils import *
import os
from rgbt.vis import draw_radar, draw_plot
from rgbt import __file__ as basepath
_basepath = os.path.dirname(basepath)


def initial_gt_file(gt_path:str, seqs:list, v_name:str, i_name:str, bbox_trans):
    res = {}
    for seq_name in seqs:
        serial_v = load_text(os.path.join(gt_path, seq_name, v_name))
        serial_i = load_text(os.path.join(gt_path, seq_name, i_name))
        seq_serial = {'visible': serial_process(bbox_trans, serial_v), 'infrared': serial_process(bbox_trans,serial_i)}
        res[seq_name] = seq_serial
    return res


def initial_result_file(path:str, seqs:list, bbox_trans, prefix=''):
    res = {}
    for seq_name in seqs:
        serial = load_text(os.path.join(path, prefix+seq_name+'.txt')).round(0)
        res[seq_name] = serial_process(bbox_trans, serial)
    return res



class TrackerResult:
    """
    Your tracking result.
    """
    def __init__(self, tracker_name, path:str, seqs:list, prefix:str, bbox_type:str) -> None:
        self.tracker_name = tracker_name
        self.seqs_name = seqs
        self.bbox_transfun = bbox_type_trans(bbox_type, 'ltwh')
        self.seqs_result = initial_result_file(path, seqs, self.bbox_transfun, prefix)
        self.bbox_type = 'ltwh'

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.seqs_result[self.seqs_name[index]]
        elif isinstance(index, str):
            return self.seqs_result[index]
        else:
            raise KeyError

    def __len__(self):
        return len(self.seqs_name)


class BaseRGBTDataet:
    """
    ground truth.
    """
    def __init__(self, gt_path:str, seqs:list, bbox_type:str, v_name=None, i_name=None) -> None:
        """
        [in] gt_path - str
            The ground truth file path.
        [in] seqs - list
            A list contain all sequence name in one dataset.
        [in] bbox_type - str
            Default is 'ltwh' (top left corner coordinates with width and height), you can also 
            choose 'ltrb' (top left corner and bottom left corner coordinates), 'xywh' (center 
            point coordinates with width and height). 
        [in] v_name - str
            The ground truth file name of visible images.
        [in] i_name - str
            The ground truth file name of infrared images.
        """
        self.gt_path = gt_path

        self.bbox_transfun = bbox_type_trans(bbox_type, 'ltwh')
        self.bbox_type = 'ltwh'

        self.seqs_name = seqs
        self.ALL = tuple(self.seqs_name)
        if v_name!=None and i_name!=None:
            self.seqs_gt = initial_gt_file(self.gt_path, seqs, v_name, i_name, self.bbox_transfun)    # ground truth
        else:
            self.seqs_gt = initial_result_file(self.gt_path, self.seqs_name, self.bbox_transfun, prefix='')

        self.trackers = {}


    def __len__(self):
        return len(self.seqs_name)
    

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.seqs_gt[self.seqs_name[index]]
        elif isinstance(index, str):
            return self.seqs_gt[index]
        else:
            raise KeyError


    def __call__(self, tracker_name, result_path:str, seqs=None, prefix='', bbox_type='ltwh') -> TrackerResult:
        """
        Return the tracker result instance.
        """
        if seqs==None:
            seqs=self.seqs_name
        self.trackers[tracker_name] = TrackerResult(tracker_name, result_path, seqs, prefix, bbox_type)
        return self.trackers[tracker_name]


    def choose_serial_by_att(self, attr):
        raise ImportError


    def get_attr_list(self):
        raise ImportError


    def draw_attributeRadar(self, metric_fun, filename, **argdict):
        """
        Draw a radar chart with all challenge attributes.
        """
        result = [[tracker_name, []] for tracker_name in self.trackers.keys()]
        for attr in self.get_attr_list():
            dict = metric_fun(seqs=getattr(self, attr))
            for i,(k,v) in enumerate(dict.items()):
                result[i][1].append(v[0])

        draw_radar(result=result, attrs=self.get_attr_list(), fn=filename, **argdict)


    def draw_plot(self, axis, metric_fun, filename, y_max:float, y_min:float, title=None, 
                  seqs=None, loc="best", rank="descend", **argdict):
        if seqs==None:
            seqs = self.ALL
        
        result = [[tracker_name, []] for tracker_name in self.trackers.keys()]
        dict = metric_fun(seqs=seqs)
        vals = []
        for i,(k,v) in enumerate(dict.items()):
            vals.append(v[0])
            result[i][0]+=f"[{round(v[0],3)}]"
            result[i][1]=v[1].mean(0)
        if rank=="descend":
            idx = sorted(range(len(vals)), key=lambda x:vals[x], reverse=True)
        else:
            idx = sorted(range(len(vals)), key=lambda x:vals[x], reverse=False)
        result = [result[i] for i in idx]
        
        draw_plot(axis=axis, result=result, fn=filename, title=title, y_max=y_max, y_min=y_min, loc=loc, **argdict)