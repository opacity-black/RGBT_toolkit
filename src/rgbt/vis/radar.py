import matplotlib.pyplot as plt
import numpy as np

from matplotlib import rc
from rgbt.vis.draw_utils import COLOR, MARKER_STYLE

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=False)

def draw_radar(result:list, attrs:list, fn:str, title=''):
    """
    Parameter
    ---
    result: [tracker_name - str, val - list]\r
    attrs: challenge attributes name\r
    fn: the image file name.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    angles = np.linspace(0, 2*np.pi, len(attrs)+1, endpoint=True)

    attr2value = []
    for i, (tracker_name, val) in enumerate(result):
        attr2value.append(val)
    attr2value = np.array(attr2value)   # tracker_num, attr_num
    max_value = np.max(attr2value, axis=0)
    min_value = np.min(attr2value, axis=0)
    for i, (tracker_name, val) in enumerate(result):
        val = [*val, val[0]]    # Close the radar chart
        plt.plot(angles, val, linestyle='-', color=COLOR[i], marker=MARKER_STYLE[i],
                label=tracker_name, linewidth=1.5, markersize=6)

    attr_value = []
    for attr, maxv, minv in zip(attrs, max_value, min_value):
        attr_value.append(attr + "\n({:.3f},{:.3f})".format(minv, maxv))

    ax.set_thetagrids(angles[:-1] * 180/np.pi, attr_value)
    ax.spines['polar'].set_visible(False)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5,-0.07), frameon=False, ncol=5)
    ax.grid(b=True, c='gray', linestyle='--')
    # ax.set_ylim(np.min(min_value)-0.05, np.max(max_value)+0.05)
    ax.set_rlim(np.min(min_value)-0.04, np.max(max_value)+0.02)
    ax.set_title(title)
    # ax.set_yticks([])
    ax.tick_params('y', labelleft=False)
    # plt.show()
    plt.savefig(fn, dpi=300)

