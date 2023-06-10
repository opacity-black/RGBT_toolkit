from rgbt import LasHeR

lasher = LasHeR()

"""
LasHeR have 3 benchmarks: PR, NPR, SR
"""

# Register your tracker
lasher(
    tracker_name="APFNet",       # Result in paper: 50.0, 43.9, 36.2
    result_path="./result/LasHeR/APFNet", 
    bbox_type="ltwh")
lasher(
    tracker_name="mfDiMP",       # Result in paper: 44.7, 39.5, 34.3
    result_path="./result/LasHeR/mfDiMP", 
    bbox_type="ltwh")

# Evaluate multiple trackers
pr_dict = lasher.PR()
print(pr_dict["APFNet"][0])
print(pr_dict["mfDiMP"][0])

npr_dict = lasher.NPR()
print(npr_dict["APFNet"][0])
print(npr_dict["mfDiMP"][0])

sr_dict = lasher.SR()
print(sr_dict["APFNet"][0])
print(sr_dict["mfDiMP"][0])

lasher.draw_plot(metric_fun=lasher.PR)
lasher.draw_plot(metric_fun=lasher.NPR)
lasher.draw_plot(metric_fun=lasher.SR)