from rgbt import GTOT
from rgbt.utils import RGBT_start,RGBT_end

RGBT_start()
gtot = GTOT()

# Register your tracker
gtot(
    tracker_name="JMMAC",       # Result in paper: 90.2, 73.2
    result_path="./result/GTOT/JMMAC", 
    bbox_type="ltwh",
    prefix="JMMAC_")

gtot(
    tracker_name="APFNet",      # Result in paper: 90.5, 73.7
    result_path="./result/GTOT/APFNet", 
    bbox_type="corner",
    prefix="")

gtot(
    tracker_name="DAFNet",      # Result in paper: 89.1, 71.2
    result_path="./result/GTOT/DAFNet", 
    bbox_type="corner",
    prefix="DAFNet-234_")

# Evaluate multiple trackers
pr_dict = gtot.MPR()
print(pr_dict["JMMAC"][0])
print(pr_dict["APFNet"][0])
print(pr_dict["DAFNet"][0])

# Evaluate single tracker
jmmac_sr,_ = gtot.MSR("JMMAC")
print("JMMAC MSR:\t", jmmac_sr)
apf_sr,_ = gtot.MSR("APFNet")
print("APFNet MSR:\t", apf_sr)
daf_sr,_ = gtot.MSR("DAFNet")
print("DAFNet MSR:\t", daf_sr)

# Draw a curve plot
gtot.draw_plot(metric_fun=gtot.MPR)
gtot.draw_plot(metric_fun=gtot.MSR)

RGBT_end()