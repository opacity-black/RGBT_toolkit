from dataset import lasher

# Register your tracker
lasher(
    tracker_name="APFNet", 
    result_path="./result/LasHeR/APFNet", 
    bbox_type="ltwh")
lasher(
    tracker_name="mfDiMP", 
    result_path="./result/LasHeR/mfDiMP", 
    bbox_type="ltwh")

lasher.draw_plot(metric_fun=lasher.PR)
lasher.draw_plot(metric_fun=lasher.SR)