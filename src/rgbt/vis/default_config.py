from collections import namedtuple
from numpy import ndarray
import numpy as np
from typing import Any,Union
import json


class Setting:
    def __init__(self, 
                # global param
                dpi:int = 300,                              # 分辨率
                enable_saveimg = True,                        # 保存文件
                filename:str = "default",
                fig_size:tuple[float, float] = (6,5.5),     # 图像大小
                legend_loc:str = "lower left",
                legend_fontsize:int=14,
                legend_bold:bool=False,
                title:Union[str, list] = "default",         # 多图时采用列表
                title_fontsize:int=20,
                title_bold:bool=True,
                ) -> None:
        self.dpi = dpi
        self.enable_saveimg = enable_saveimg
        self.filename = filename
        self.legend_loc = legend_loc
        self.title = title
        self.legend_bold = legend_bold
        self.fig_size = fig_size
        self.title_fontsize = title_fontsize
        self.legend_fontsize = legend_fontsize
        self.title_bold = title_bold
        

    def __repr__(self) -> str:
        return str(self.__dict__)

    def save(self, name:str) -> None:
        with open(name, 'w') as f:
            json.dump(self.__dict__, f)
            
    def load(self, name:str) -> None:
        with open(name, 'r') as f:
            val = json.load(f)
        for k,v in self.__dict__.items():
            if k in val:
                self.__dict__[k] = v
            else:
                raise BaseException(f"Unknow attribute \"{k}\".")


class PlotSetting(Setting):
    def __init__(self, 
                # global param
                dpi:int = 300,
                enable_saveimg = True,                        # 保存文件
                filename:str = "default_plot",
                fig_size:tuple[float, float] = (6,5.5),
                legend_loc:str = "lower left",
                legend_fontsize:int=14,
                legend_bold:bool=False,
                # plot param (pr/sr/npr)
                axis:ndarray=np.array([]),   
                ylim:tuple[float, float]=(0.0, 1.0),
                linewidth:int=3,
                title:str = "title",
                xlabel:str = "xlabel",
                ylabel:str = "ylabel",
                title_fontsize:int=20,
                xlabel_fontsize:int=20,
                ylabel_fontsize:int=20,
                title_bold:bool=True,
                xlabel_bold:bool=True,
                ylabel_bold:bool=True,
                xticks:Any=[],  # x坐标轴刻度
                yticks:Any=[],
                xtick_fontsize=None,
                ytick_fontsize=None,
                font="TimesNewRoman",
                ) -> None:
        super().__init__(dpi, enable_saveimg, filename, fig_size, legend_loc, legend_fontsize, legend_bold, 
                         title, title_fontsize, title_bold)
        self.axis = axis
        self.xticks = xticks
        self.yticks = yticks
        self.xtick_fontsize = xtick_fontsize
        self.ytick_fontsize = ytick_fontsize
        self.ylim = ylim
        self.linewidth = linewidth
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.xlabel_fontsize = xlabel_fontsize
        self.ylabel_fontsize = ylabel_fontsize
        self.xlabel_bold = xlabel_bold
        self.ylabel_bold = ylabel_bold
        self.font = font



class RadarSetting(Setting):
    def __init__(self, 
                 # base
                dpi: int = 300, 
                enable_saveimg = True,                        # 保存文件
                filename: str = "default_radar", 
                fig_size: tuple[float, float] = (3, 3), 
                 # legend
                legend_loc: str = "lower center",   # 'best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center'
                bbox_to_anchor:tuple[float, float] = None,   # 图例的相对位置(x,y)，该项的优先级更高    # type:ignore
                legend_fontsize: int = 7, 
                legend_bold: bool = False, 
                frameon:bool=True,             # 图例背景
                 # title
                title: str = "title", 
                title_fontsize: int = 14,
                # radar param
                enable_ticks:bool=False,        # 刻度显示
                grid_type:str='straight',       # 网格线样式
                fill_color:bool=True,           # 启用颜色填充
                fill_alpha:float=0.18,          # 填充颜色的透明度
                fill_linewidth:float=2.5,       # 填充块边界
                fill_markersize:int=5,          # 填充边界的标记点半径
                # attr
                attr_li=[],                     # 挑战属性列表
                attr_fontsize:int=7,            # 属性字体大小
                attr_bold:bool=False,           # 属性字体加粗
                showMinMaxVal:bool=True,        # 是否在属性标签下展示得分的最小值和最大值
                distance:float=0.,             # 属性距离坐标的距离
                # other
                rlabel_position:int=-140,       # 主轴方向
                ytick_fontsize=6,               # 刻度字体大小
                board:tuple=(0.8, 0.15, 0.1, 0.9, 0.37),                 # 调整边距, 上下左右+子图边距
                showAbsVal:bool=False,          # 展示相对值还是绝对值，默认展示相对值
                 ) -> None:
        super().__init__(dpi, enable_saveimg, filename, fig_size, legend_loc, legend_fontsize, legend_bold, title, title_fontsize)
        self.attr_li = attr_li
        self.frameon = frameon
        self.enable_ticks = enable_ticks
        self.grid_type = grid_type
        self.fill_color = fill_color
        self.fill_alpha = fill_alpha
        self.bbox_to_anchor = bbox_to_anchor
        self.attr_fontsize = attr_fontsize
        self.attr_bold = attr_bold
        self.rlabel_position = rlabel_position
        self.ytick_fontsize = ytick_fontsize
        self.board = board
        self.fill_markersize = fill_markersize
        self.fill_linewidth = fill_linewidth
        self.showAbsVal = showAbsVal
        self.showMinMaxVal = showMinMaxVal
        self.distance = distance


PR_Config = {
    "title_fontsize": 20,
    "x_axis_fontsize": 20,
    "y_axis_fontsize": 20,
    "legend_fontsize": 20,
    "title_bold": True,
    "x_axis_bold": True,
    "y_axis_bold": True,
    "legend_bold": False,
}

SR_Config = {
    "title_fontsize": 20,
    "x_axis_fontsize": 20,
    "y_axis_fontsize": 20,
    "legend_fontsize": 20,
    "title_bold": True,
    "x_axis_bold": True,
    "y_axis_bold": True,
    "legend_bold": False,
}

Radar_Config = {

}


def dict_to_object(dict):
    return namedtuple("Object", dict.keys())(**dict)

def updateConfig(configName):
    config = dict_to_object(SR_Config)

def get_SR_Setting():
    SR_PlotSetting = PlotSetting()
    SR_PlotSetting.title = "Success Plot"
    SR_PlotSetting.legend_loc = "lower left"
    SR_PlotSetting.xlabel = "overlap threshold"
    SR_PlotSetting.ylabel = "Success Rate"
    return SR_PlotSetting


def get_PR_Setting():
    PR_PlotSetting = PlotSetting()
    PR_PlotSetting.title = "Precision Plot"
    PR_PlotSetting.legend_loc = "lower right"
    PR_PlotSetting.xlabel = "Location error threshold"
    PR_PlotSetting.ylabel = "Precision"
    return PR_PlotSetting


def get_Radar_Setting():
    radarPlotSetting = RadarSetting()
    radarPlotSetting.title = 'Attribute Score'
    radarPlotSetting.legend_loc = "upper center"
    return radarPlotSetting


if __name__=="__main__":
    a=get_Radar_Setting()
    a.save("default_radar.json")
    a.load("default_radar.json")
    
    b=get_PR_Setting()
    try:
        b.load("default_radar.json")
    except BaseException as e:
        print(e)
