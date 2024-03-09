from collections import namedtuple
from numpy import ndarray
import numpy as np
from typing import Any

class Setting:
    def __init__(self, 
                # global param
                dpi:int = 300,
                filename:str = "default",
                fig_size:tuple[float, float] = (6,5.5),
                legend_loc:str = "lower left",
                legend_fontsize:int=14,
                legend_bold:bool=False,
                # plot param (pr/sr/npr)
                axis:ndarray=np.array([]),   
                ylim:tuple[float, float]=(0.0, 1.0),
                linewidth:int=3,
                title:str = "default",
                xlabel:str = "default",
                ylabel:str = "default",
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
                # radar param
                ) -> None:
        self.axis = axis
        self.xticks = xticks
        self.yticks = yticks
        self.xtick_fontsize = xtick_fontsize
        self.ytick_fontsize = ytick_fontsize
        self.ylim = ylim
        self.dpi = dpi
        self.linewidth = linewidth
        self.filename = filename
        self.legend_loc = legend_loc
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.fig_size = fig_size
        self.title_fontsize = title_fontsize
        self.xlabel_fontsize = xlabel_fontsize
        self.ylabel_fontsize = ylabel_fontsize
        self.legend_fontsize = legend_fontsize
        self.title_bold = title_bold
        self.xlabel_bold = xlabel_bold
        self.ylabel_bold = ylabel_bold
        self.legend_bold = legend_bold

    def __repr__(self) -> str:
        return str(self.__dict__)

# GlobalConfig = {
#     "title_fontsize": 20,
#     "x_axis_fontsize": 20,
#     "y_axis_fontsize": 20,
#     "legend_fontsize": 20,
#     "title_bold": True,
#     "x_axis_bold": True,
#     "y_axis_bold": True,
#     "legend_bold": False,
# }

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
    SR_PlotSetting = Setting()
    SR_PlotSetting.title = "Success Plot"
    SR_PlotSetting.legend_loc = "lower left"
    SR_PlotSetting.xlabel = "overlap threshold"
    SR_PlotSetting.ylabel = "Success Rate"
    return SR_PlotSetting


def get_PR_Setting():
    PR_PlotSetting = Setting()
    PR_PlotSetting.title = "Precision Plot"
    PR_PlotSetting.legend_loc = "lower right"
    PR_PlotSetting.xlabel = "Location error threshold"
    PR_PlotSetting.ylabel = "Precision"
    return PR_PlotSetting