import matplotlib.pyplot as plt
import numpy as np

from rgbt.vis.draw_utils import COLOR, LINE_STYLE
from rgbt.vis.font import *
from rgbt.vis.default_config import PlotSetting

def plot(result:list[tuple[str, np.ndarray]], setting:PlotSetting):
    axis = setting.axis
    fig = plt.figure(figsize=setting.fig_size)
    ax = fig.add_subplot(111)
    for i,(name,val) in enumerate(result):
        j = i//len(COLOR)
        ax.plot(axis, val, color=COLOR[i], linestyle=LINE_STYLE[j], linewidth=setting.linewidth, label=name)
    ax.set_xlim(xmax=max(axis), xmin=min(axis))
    ax.set_ylim(ymin=setting.ylim[0], ymax=setting.ylim[1])

    # 坐标轴设置
    if setting.xticks!=[]:
        xticks = setting.xticks
    else:
        xticks = ax.get_xticks()
    if setting.yticks!=[]:
        yticks = setting.yticks
    else:
        yticks = ax.get_yticks()
    if setting.xticks!=[] or setting.xtick_fontsize!=None:
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, fontsize=setting.xtick_fontsize)
    if setting.yticks!=[] or setting.ytick_fontsize!=None:
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticks, fontsize=setting.ytick_fontsize)

    ax.set_title(setting.title, fontdict=TimesNewRoman(setting.title_fontsize, setting.title_bold)) # type: ignore
    ax.set_xlabel(setting.xlabel, fontdict=TimesNewRoman(setting.xlabel_fontsize, setting.xlabel_bold))
    ax.set_ylabel(setting.ylabel, fontdict=TimesNewRoman(setting.ylabel_fontsize, setting.ylabel_bold))
    ax.legend(loc=setting.legend_loc, prop=TimesNewRoman(setting.legend_fontsize, setting.legend_bold))
    fig.savefig(setting.filename, dpi=setting.dpi)



if __name__=="__main__":
    data = [
        ("A", np.array([0.9, 0.8, 0.78, 0.75, 0.6, 0.3, 0.0])),
        ("B", np.array([0.92, 0.82, 0.78, 0.7, 0.55, 0.28, 0.0])),
    ]
    setting = PlotSetting()
    setting.axis = np.arange(7)
    plot(data, setting)