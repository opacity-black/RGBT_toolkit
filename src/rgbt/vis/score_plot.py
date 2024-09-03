import matplotlib.pyplot as plt
import numpy as np
from sympy import Le

if __name__=="__main__":
    from draw_utils import COLOR, LINE_STYLE
    from font import TimesNewRoman
    from default_config import ScorePlotSetting
else:
    from rgbt.vis.draw_utils import COLOR, LINE_STYLE
    from rgbt.vis.font import TimesNewRoman
    from rgbt.vis.default_config import ScorePlotSetting


def avg_smooth(array, k=3):
    f1 = lambda x: x if x>0 else 0
    f2 = lambda x: x if x<len(array) else len(array)
    new_array = np.array(array)
    for i in range(len(array)):
        new_array[i] = np.array(array[f1(i-k//2): f2(i+k//2)]).mean()
    return new_array
    

def score_plot(result:dict, setting:ScorePlotSetting):
    """
    result:{
        seq_num: int,
        seq_li: [
            [$seq_name: str,
            $trackerA: list[float], 
            $trackerB: list[float],]
        ],
    }
    """
    fig = plt.figure(dpi=setting.dpi, figsize=setting.fig_size,)
    gs = fig.add_gridspec(result['seq_num'],1)
    subplot_size = result['seq_num']
    first_plot_idx = int(str(subplot_size)+str(11))
    tracker_label = list(result[list(result.keys())])
    # axs = [fig.add_subplot(first_plot_idx+i) for i in range(subplot_size)]
    axs = [fig.add_subplot(gs[i:i+1,0]) for i in range(subplot_size)]

    for SEQ, ax in zip(result.keys(), axs):
        if SEQ=="seq_num":
            continue

        # 绘图
        # COLORS = ['b', 'm', 'g', 'r', 'k']
        # COLORS = [
        #     # (219, 49, 36),
        #     # (75, 116, 178),
        #     # (2, 48, 71),
        #     # (251, 132, 2)
        # [112, 173, 71],
        # [255, 192, 0],
        # [0, 176, 240],
        # # [239, 99, 86],  # 红色
        # [237, 125, 47],
        # [112, 48, 160],
        # ]
        # COLORS = np.array(COLORS)/255.
        COLORS = COLOR

        # different tracker
        max_L = 0
        for i, (tracker, val_li) in enumerate(result[SEQ].items()):
            LEN=min(len(val_li), setting.max_len)
            if LEN>max_L:
                max_L = LEN
            X = np.arange(0, LEN, 1)
            y = np.array(val_li[:LEN])*100
            y_smooth = avg_smooth(y, k=setting.smooth_strongth)           # 进行简单的平滑
            line_type = '-'
            # line_type = '--'
            ax.plot(X, y_smooth, label=tracker, linewidth=setting.linewidth, color=COLORS[i], 
                    linestyle=line_type, alpha=setting.alpha)

        ax.set_xlim(xmax=max_L, xmin=0.)
        ax.set_ylim(ymax=100., ymin=0.)
        ax.set_title(SEQ, fontdict=TimesNewRoman(18), loc='left')
        if ax.get_subplotspec().is_last_row():              # type: ignore
            ax.set_xlabel(setting.xlabel, fontdict=TimesNewRoman(setting.xlabel_fontsize, setting.xlabel_bold))
        ax.set_ylabel(setting.ylabel, fontdict=TimesNewRoman(setting.ylabel_fontsize, setting.ylabel_bold))
        # ax.set_xticklabels(ax.get_xticklabels(), fontsize=16)
        # ax.set_yticklabels(ax.get_yticklabels(), fontsize=16)
        [item.set_fontsize(20) for item in ax.get_xticklabels()]
        [item.set_fontsize(20) for item in ax.get_yticklabels()]
        
        # bg = np.array(bg, dtype=np.uint8)
        # ax.imshow(bg, extent=[0,LEN,0,100], alpha=BG_ALPHA, aspect='auto', interpolation='nearest')      # 添加背景

    # fig.tight_layout()
    line, label = fig.axes[-1].get_legend_handles_labels()      # 读取图里的label
    # custom_lines = [Line2D([0], [0], color=np.array(color)/255, lw=12) for color in MISS_STATE_COLOR.values()]      # 自定义色块label
    # custom_lines = [Patch(facecolor=np.array(color)/255, edgecolor='grey') for color in MISS_STATE_COLOR.values()]      # 自定义色块label
    # all_line = []; all_label = []
    # for i in range(len(custom_lines)+len(line)):
    #     all_line.append(line[i//2] if i%2 else custom_lines[i//2])
    #     all_label.append(label[i//2] if i%2 else MISS_STATE[i//2])
    # for i in range(len(all_label)):
    #     if 'copy' in all_label[i]:
    #         all_label[i] = all_label[i].replace('copy', 'w/ copy')
    #     if 'zero' in all_label[i]:
    #         all_label[i] = all_label[i].replace('zero', 'w/ zero')
    # fig.legend(all_line, all_label, bbox_to_anchor=setting.bbox_to_anchor, ncol=5, frameon=setting.frameon,
    #             loc=setting.legend_loc, prop=TimesNewRoman(setting.legend_fontsize, setting.legend_bold))
    
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
    # fig.subplots_adjust(top=setting.board[0], 
    #                     bottom=setting.board[1], 
    #                     left=setting.board[2], 
    #                     right=setting.board[3], 
    #                     wspace=setting.board[4])
    if setting.enable_saveimg:
        fig.savefig(setting.filename)
    else:
        fig.show()


if __name__=="__main__":
    result = {
        "seq_num": 2,
        "seq_A":{
            "trackerA": np.random.random(100),
            "trackerB": np.random.random(100),
        },
        "seq_B":{
            "trackerA": np.random.random(100),
            "trackerB": np.random.random(100),
        }
    }
    setting = ScorePlotSetting()
    score_plot(result, setting)