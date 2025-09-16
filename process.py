#程宇20250910
#使用新版本的yolov11进行训练、测试
#目前可以使用摄像头、图片等形式的识别
from matplotlib.pyplot import imread
from ultralytics import YOLO
import cv2

# Load a pretrained YOLO11n model
model = YOLO(r"yolo11n.pt")

##
#camera detection
results = model.predict(source="0", classes=[0], show=True)




# ##自适应图片识别与显示
# # Define path to the image file
# source = cv2.imread(r"/datasets/data/valid\images\screenshot_15_png.rf.c39f6ad49457744c6a567ddb8602d89e.jpg", cv2.IMREAD_COLOR)
#
# results = model.predict(source, classes=[1])
# annotated_frame = results[0].plot()
# # 方法1: 指定目标尺寸
# h, w = source .shape[:2]
# max_width = 1920
# max_height = 1080
# # 计算缩放比例
# scale = min(max_width / w, max_height / h, 1.0)  # 不超过1.0（不放大）
# new_w = int(w * scale)
# new_h = int(h * scale)
# annotated_frame = cv2.resize(annotated_frame, (new_w, new_h))
# cv2.imshow('YOLO Detection', annotated_frame)
# print("图片已显示，按任意键继续...")
# cv2.waitKey(0)  # 程序会停在这里等待按键




