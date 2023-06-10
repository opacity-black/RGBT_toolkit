from rgbt import RGBT210

rgbt210 = RGBT210()

# Register your tracker
rgbt210(
    tracker_name="SOWP",        # Result in paper: 59.9, 37.9
    result_path="./result/RGBT210/SOWP", 
    bbox_type="ltwh",
    prefix="SOWP_")

# Evaluate multiple trackers

sr_dict = rgbt210.SR()
print(sr_dict["SOWP"][0])

pr_dict = rgbt210.PR()
print(pr_dict["SOWP"][0])

rgbt210.draw_plot(metric_fun=rgbt210.PR)
