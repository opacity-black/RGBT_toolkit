from rgbt import RGBT234
import time

st = time.time()
rgbt234 = RGBT234()

# Register your tracker
rgbt234(
    tracker_name="TFNet",       # Result in paper: 80.6, 56.0
    result_path="../result/RGBT234/TFNet", 
    bbox_type="corner",
    prefix="TFNet_")

rgbt234(
    tracker_name="APFNet",      # Result in paper: 82.7, 57.9
    result_path="../result/RGBT234/APFNet", 
    bbox_type="corner")


rgbt234(
    tracker_name="JMMAC",       # Result in paper: 79.0, 57.3
    result_path="../result/RGBT234/JMMAC", 
    bbox_type="ltwh",
    prefix="JMMAC_234_final_")

# Evaluate multiple trackers
pr_dict = rgbt234.MPR()
print(pr_dict["APFNet"][0])
print(pr_dict["TFNet"][0])
print(pr_dict["JMMAC"][0])

# Evaluate single tracker
apf_sr,_ = rgbt234.MSR("APFNet")
print("APFNet MSR: \t", apf_sr)
tf_sr,_ = rgbt234.MSR("TFNet")
print("TFNet MSR: \t", tf_sr)
jmmac_sr,_ = rgbt234.MSR("JMMAC")
print("JMMAC MSR: \t", jmmac_sr)

print(f"Time: {time.time()-st}")    # 36.6 -> 35.3

# Evaluate single challenge
pr_tc_dict = rgbt234.MPR(seqs=rgbt234.TC)
sr_tc_dict = rgbt234.MSR(seqs=rgbt234.TC)

# Draw a radar chart of all challenge attributes
rgbt234.draw_attributeRadar(metric_fun=rgbt234.MPR, filename="RGBT234_MPR_radar.png")
rgbt234.draw_attributeRadar(metric_fun=rgbt234.MSR)     # this is ok

# Draw a curve plot
rgbt234.draw_plot(metric_fun=rgbt234.MPR)
rgbt234.draw_plot(metric_fun=rgbt234.MSR)

print(f"Time: {time.time()-st}")    # 149.5 -> 145.5