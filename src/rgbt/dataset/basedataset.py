
from rgbt.utils import *
import os
from rgbt.vis import radar as draw_radar
from rgbt.vis import plot as draw_plot
from rgbt import __file__ as basepath
_basepath = os.path.dirname(basepath)


def initial_gt_file(gt_path:str, seqs:list, v_name:str, i_name:str, bbox_trans) -> dict:
    res = {}
    for seq_name in seqs:
        serial_v = load_text(os.path.join(gt_path, seq_name, v_name))
        serial_i = load_text(os.path.join(gt_path, seq_name, i_name))
        if bbox_trans!=None:
            res[seq_name] = {
                'visible': list(map(bbox_trans, serial_v)),
                'infrared': list(map(bbox_trans, serial_i)),
            }
        else:
            res[seq_name] = {'visible': serial_v, 'infrared': serial_i}
    return res


def initial_result_file(path:str, seqs:list, bbox_trans, prefix=''):
    res = {}
    for seq_name in seqs:
        serial = load_text(os.path.join(path, prefix+seq_name+'.txt')).round(0)
        if bbox_trans!=None:
            res[seq_name] = list(map(bbox_trans, serial))
        else:
            res[seq_name] = serial
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


    def get_attr_list(self) -> Union[tuple, list]:
        raise ImportError


    def radar(self, metric_fun, radarSetting, **argdict):
        """
        Draw a radar chart with all challenge attributes.
        """
        result = [[tracker_name, []] for tracker_name in self.trackers.keys()]
        for attr in self.get_attr_list():
            dict = metric_fun(seqs=getattr(self, attr))
            for i,(k,v) in enumerate(dict.items()):
                result[i][1].append(round(v[0]*100, 1))

        draw_radar(results=[result], setting=radarSetting)


    def plot(self, metric_fun, plotSetting, seqs=None, descend=True, **argdict):
        """
        Args:
            metric_fun:
                评估函数，输入需要测评的序列，输出测评结果
            plotSetting:
                绘图设置
            seqs:
                需要测试的序列，默认为全部序列
            descend:
                降序排列跟踪器，默认为真
        """
        if seqs==None:
            seqs = self.ALL
        
        trk_dict:dict[str, tuple] = metric_fun(seqs=seqs)

        trk_plot_data = []
        for trk_name, trk_res in trk_dict.items():
            trk_label = f"{trk_name} [{round(trk_res[0],3)}]"
            trk_plot_data.append((trk_label, trk_res[1].mean(0)))

        # 按性能对跟踪器排序
        trk_plot_data = sorted(trk_plot_data, key=lambda x:float(x[0].split("[")[-1][:-1]), reverse=descend)
        
        draw_plot(result=trk_plot_data, setting=plotSetting)