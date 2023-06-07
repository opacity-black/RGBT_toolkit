from dataset import rgbt210

# Register your tracker
rgbt210(
    tracker_name="TFNet", 
    result_path="./result/RGBT234/TFNet", 
    bbox_type="corner",
    prefix="TFNet_")

rgbt210(
    tracker_name="SOWP", 
    result_path="./result/RGBT210/SOWP", 
    bbox_type="ltwh",
    prefix="SOWP_")

# Evaluate multiple trackers

sr_dict = rgbt210.SR()
print(sr_dict["TFNet"][0])
print(sr_dict["SOWP"][0])


pr_dict = rgbt210.PR()
print(pr_dict["TFNet"][0])
print(pr_dict["SOWP"][0])

rgbt210.draw_plot(metric_fun=rgbt210.PR)
