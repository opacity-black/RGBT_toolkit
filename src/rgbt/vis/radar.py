import matplotlib.pyplot as plt
import numpy as np
if __name__=="__main__":
    from default_config import RadarSetting
    from font import TimesNewRoman
else:
    from rgbt.vis.default_config import RadarSetting
    from rgbt.vis.font import TimesNewRoman

# from matplotlib import rc
from rgbt.vis.draw_utils import COLOR, MARKER_STYLE

# rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
# rc('text', usetex=False)


def radar(results:list, setting:RadarSetting,):
    """
    Parameter
    ---
    results: [
        subplot1: [ [tracker_name - str, val - list], ... ], \r
        subplot2: [...]  \r
        ]\r
    """
    grid_type = setting.grid_type
    assert grid_type in ['curve', 'straight', None]

    subplot_size = len(results)
    fig = plt.figure(figsize=setting.fig_size, dpi=setting.dpi)
    tracker_label = [name for name,_ in results[0]]
        
    first_plot_idx = int(str(1)+str(subplot_size)+str(1))
    axs = [fig.add_subplot(first_plot_idx+i, projection='polar') for i in range(subplot_size)]
    # axs = fig.subplots(nrows=1, ncols=len(results))
    if isinstance(setting.title, str):
        titles = [setting.title] 
    titles = titles if titles!=None else ['']*len(results)
    for ax, result, title in zip(axs, results, titles):
        angles = np.linspace(0, 2*np.pi, len(setting.attr_li)+1, endpoint=True)

        attr2value = []
        for i, (tracker_name, val) in enumerate(result):
            attr2value.append(val)

        if getattr(setting, "showAbsVal", False):
            attr2value = np.array(attr2value)   # tracker_num, attr_num
            max_value = np.max(attr2value, axis=0)
            min_value = np.min(attr2value, axis=0)
        else:
            attr2value_abs = np.array(attr2value)   # tracker_num, attr_num
            attr2value = attr2value_abs/attr2value_abs.max(0)
            max_value = np.max(attr2value_abs, axis=0)
            min_value = np.min(attr2value_abs, axis=0)

        for i, (tracker_name, val) in enumerate(result):
            # val = [*val, val[0]]    # Close the radar chart
            val = [*attr2value[i], attr2value[i][0]]    # Close the radar chart
            ax.plot(angles, val, linestyle='-', color=COLOR[i], marker='o',
                    label=tracker_name, linewidth=setting.fill_linewidth, markersize=setting.fill_markersize)
            if setting.fill_color:
                ax.fill(angles, val, alpha=setting.fill_alpha, color=COLOR[i])

        attr_value = []
        for attr, maxv, minv in zip(setting.attr_li, max_value, min_value):
            if setting.showMinMaxVal:
                attr_value.append(attr + "\n({:.1f},{:.1f})".format(minv, maxv))
            else:
                attr_value.append(attr)

        # 设置刻度
        min_v, max_v = np.min(attr2value), np.max(attr2value)
        y_ticks = np.arange(min_v//0.03*0.03, max_v+0.04, 0.03, dtype=np.float32)
        y_ticks[-1]=1.01
        # y_ticks = np.arange(40 if min_v>40 else min_v//10*10, max_v+10, 10, dtype=np.int32)
        x_ticks = angles[:-1] * 180/np.pi
        if setting.enable_ticks:
            ax.set_yticks(y_ticks)
            ax.set_yticklabels(y_ticks, fontsize=setting.ytick_fontsize)
            ax.tick_params('y', labelleft=True)                                  # 显示y轴刻度
            ax.set_rlabel_position(setting.rlabel_position)      # type: ignore  # 刻度的方向
        else:
            ax.tick_params('y', labelleft=False)

        # 设置网格线样式
        ax.spines['polar'].set_visible(False)                       # 隐藏最外圈的圆
        if grid_type==None:
            ax.grid(False)
        elif grid_type=='curve':
            ax.grid(b=True, c='gray', linestyle='-.', )
        elif grid_type=='straight':
            ax.grid(False)
            for item in y_ticks:
                ax.plot(angles, [item]*len(angles), linestyle='-', color='grey', lw=0.8, alpha=0.6)
            for item in x_ticks:
                ax.plot([item*np.pi/180]*2, [y_ticks[0], y_ticks[-1]], linestyle='-', color='grey', lw=0.8, alpha=0.6)

        ax.set_thetagrids(x_ticks, attr_value, fontsize=setting.attr_fontsize, fontname=TimesNewRoman()['family'])      # type: ignore # 放置属性名词
        ax.set_theta_zero_location('N')                             # type: ignore # 设置主轴朝向
        # ax.set_ylim(np.min(min_value)-0.05, np.max(max_value)+0.05)
        ax.set_rlim(y_ticks[0], y_ticks[-1]+setting.distance)                      # type: ignore
        ax.set_title(title, fontdict=TimesNewRoman(setting.title_fontsize, setting.title_bold))
        
    line, label = fig.axes[-1].get_legend_handles_labels()

    if setting.bbox_to_anchor!=None:
        fig.legend(line, label, 
                bbox_to_anchor=setting.bbox_to_anchor, 
                frameon=setting.frameon, 
                ncol=min(5, len(tracker_label)),
                prop=TimesNewRoman(setting.legend_fontsize, setting.legend_bold))  # 图例
    else:
        fig.legend(line, label, 
                loc=setting.legend_loc, 
                frameon=setting.frameon, 
                ncol=min(5, len(tracker_label)),
                prop=TimesNewRoman(setting.legend_fontsize, setting.legend_bold))  # 图例
    fig.tight_layout()                  # 避免子图间重叠
    fig.subplots_adjust(top=setting.board[0], 
                        bottom=setting.board[1], 
                        left=setting.board[2], 
                        right=setting.board[3], 
                        wspace=setting.board[4])
    if setting.enable_saveimg:
        fig.savefig(setting.filename)
    else:
        fig.show()



if __name__=="__main__":
    data = [[
        ("tA", np.array([90., 80., 78., 75., 60., 30., 60.])),
        ("tB", np.array([92., 82., 78., 70., 55., 28., 50.])),
    ]]
    setting = RadarSetting()
    setting.enable_saveimg = True
    # setting.dpi = 150
    setting.attr_li = ["A", "B", "C", "D", "E", "F", "G"]
    radar(data, setting)
    input('done')