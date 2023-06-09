from dataset import GTOT

gtot = GTOT()

# Register your tracker
gtot(
    tracker_name="JMMAC",       # Result in paper: 90.1, 73.2
    result_path="./result/GTOT/JMMAC", 
    bbox_type="ltwh",
    prefix="JMMAC_")

gtot(
    tracker_name="APFNet",       # Result in paper: 90.5, 73.7
    result_path="./result/GTOT/APFNet", 
    bbox_type="corner",
    prefix="")

# Evaluate multiple trackers
pr_dict = gtot.MPR()
print(pr_dict["JMMAC"][0])
print(pr_dict["APFNet"][0])

# Evaluate single tracker
jmmac_sr,_ = gtot.MSR("JMMAC")
print("JMMAC SR:\t", jmmac_sr)
apf_sr,_ = gtot.MSR("APFNet")
print("APFNet SR:\t", apf_sr)

# Draw a curve plot
gtot.draw_plot(metric_fun=gtot.MPR)
gtot.draw_plot(metric_fun=gtot.MSR)