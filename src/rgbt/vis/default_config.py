from collections import namedtuple
from numpy import ndarray
import numpy as np
from typing import Any,Union


class Setting:
    def __init__(self, 
                # global param
                dpi:int = 300,
                filename:str = "default",
                fig_size:tuple[float, float] = (6,5.5),
                legend_loc:str = "lower left",
                legend_fontsize:int=14,
                legend_bold:bool=False,
                title:Union[str, list] = "default",         # 多图时采用列表
                title_fontsize:int=20,
                title_bold:bool=True,
                ) -> None:
        self.dpi = dpi
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



class PlotSetting(Setting):
    def __init__(self, 
                # global param
                dpi:int = 300,
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
        super().__init__(dpi, filename, fig_size, legend_loc, legend_fontsize, legend_bold, 
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
                 dpi: int = 300, 
                 filename: str = "default_radar", 
                 fig_size: tuple[float, float] = (6, 5.5), 
                 legend_loc: str = "lower center", 
                 legend_fontsize: int = 14, 
                 legend_bold: bool = False, 
                 title: str = "title", 
                 title_fontsize: int = 20,
                # radar param
                attr_li=[],                     # 挑战属性列表
                frameon:bool=False,             # 图例背景
                enable_ticks:bool=True,         # 刻度显示
                grid_type:str='straight',       # 网格线样式
                fill_color:bool=True,           # 启用颜色填充
                fill_alpha:float=0.18,          # 填充颜色的透明度
                fill_linewidth:float=2.5,       # 填充快边界
                fill_markersize:int=10,         # 填充边界的标记点大小
                bbox_to_anchor:tuple=(0.5, 1.0),# 图例的相对位置
                attr_fontsize:int=14,           # 属性字体大小
                attr_bold:bool=False,           # 
                rlabel_position:int=-140,       # 主轴方向
                ytick_fontsize=None,            # 刻度字体大小
                board:tuple=(0.75, 0.02, 0.05, 0.95, 0.37),                 # 调整边距, 上下左右+子图边距
                 ) -> None:
        super().__init__(dpi, filename, fig_size, legend_loc, legend_fontsize, legend_bold, title, title_fontsize)
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
    radarPlotSetting.title = ''
    radarPlotSetting.legend_loc = "upper center"
    return radarPlotSetting