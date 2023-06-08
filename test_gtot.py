from dataset import GTOT

gtot = GTOT()

# Register your tracker
gtot(
    tracker_name="JMMAC",       # Result in paper: 90.1, 73.2
    result_path="./result/GTOT/JMMAC", 
    bbox_type="ltwh",
    prefix="JMMAC_")

# Evaluate multiple trackers
pr_dict = gtot.MPR()
print(pr_dict["JMMAC"][0])

# Evaluate single tracker
jmmac_sr,_ = gtot.MSR("JMMAC")
print(jmmac_sr)

# Draw a curve plot
gtot.draw_plot(metric_fun=gtot.MPR)
gtot.draw_plot(metric_fun=gtot.MSR)