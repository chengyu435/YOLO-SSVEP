import cv2
import time
from ultralytics import YOLO

# 加载 YOLO 模型
model = YOLO("yolo11n.pt")

# 打开摄像头
cap = cv2.VideoCapture(0)

# 设置摄像头分辨率（可选）
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 目标采样频率
TARGET_HZ = 60.0
FRAME_INTERVAL = 1.0 / TARGET_HZ

while True:
    start_time = time.perf_counter()

    ret, frame = cap.read()
    if not ret:
        break

    # YOLO 推理（只检测类别0，例如 person）
    results = model(frame, classes=[0], verbose=False)

    # results[0].plot() 会在 frame 上绘制检测框
    annotated_frame = results[0].plot()

    # 显示检测结果
    cv2.imshow("YOLO Detection", annotated_frame)

    # ===== 保存原始图像 & 检测结果 =====
    # 原始帧
    raw_frame = frame.copy()
    # 检测结果（xyxy坐标、类别、置信度）
    boxes = results[0].boxes.xyxy.cpu().numpy()
    classes = results[0].boxes.cls.cpu().numpy()
    confs = results[0].boxes.conf.cpu().numpy()

    # 你可以在这里保存到列表 / 写文件，供后续 SSVEP 使用
    # 例如：保存一帧的数据
    # save_data(raw_frame, boxes, classes, confs)

    # ===== 保证 60Hz 采样 =====
    elapsed = time.perf_counter() - start_time
    sleep_time = FRAME_INTERVAL - elapsed
    if sleep_time > 0:
        time.sleep(sleep_time)

    # 按 ESC 退出
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
