import matplotlib.pyplot as plt
import numpy as np

from rgbt.vis.draw_utils import COLOR, LINE_STYLE

def draw_plot(axis:np.ndarray, result:list, fn:str, title:str, y_max:float, y_min:float, loc:str, 
              x_label='', y_label=''):
    """
    Parameter
    ---
    axis: x-axis
    result: [tracker_name - str, val - list]\r
    fn: the image file name.
    loc: "upper center"
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i,(name,val) in enumerate(result):
        j = i//len(COLOR)
        ax.plot(axis, val.squeeze(), color=COLOR[i], linestyle=LINE_STYLE[j], linewidth=3, label=name)
    ax.set_xlim(xmax=max(axis), xmin=min(axis))
    ax.set_ylim(ymin=y_min, ymax=y_max)
    ax.set_xlabel(x_label, fontsize=18)
    ax.set_ylabel(y_label, fontsize=18)
    ax.set_title(title)
    ax.legend(loc=loc)
    fig.savefig(fn, dpi=300)
