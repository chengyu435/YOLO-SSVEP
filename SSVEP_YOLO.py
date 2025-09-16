##程宇20250916
#结合YOLOV11和pygame实现
#基于视觉目标追踪的多目标 SSVEP 实验范式设计
# ssvep_yolo_strict_simple.py
import sys
import math
import time
import ctypes
import pygame
import cv2
from ultralytics import YOLO

# Windows DPI 设置
if sys.platform == "win32":
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception as e:
        print("DPI awareness 设置失败：", e)

# -------- 参数 ----------
SCREEN_W = 2560
SCREEN_H = 1440
REFRESH_RATE = 60.0       # 精确帧率
FRAME_INTERVAL = 1.0 / REFRESH_RATE
STIM_RADIUS = 80
STIM_MAX_LUM = 255
STIM_MIN_LUM = 0
DEFAULT_CENTER = (SCREEN_W // 2, SCREEN_H // 2)
YOLO_MODEL_PATH = "yolo11n.pt"
CAM_W, CAM_H = 1280, 720
N_TARGETS = 3
STIM_FREQS = [6,7,8,9,10]
# ------------------------

def try_set_mode(size):
    flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
    try:
        return pygame.display.set_mode(size, flags, vsync=1)
    except TypeError:
        return pygame.display.set_mode(size, flags)

def main():
    pygame.init()
    pygame.display.set_caption("YOLO + Multi-SSVEP Strict FPS (ESC to quit)")
    screen = try_set_mode((SCREEN_W, SCREEN_H))
    pygame.mouse.set_visible(False)

    model = YOLO(YOLO_MODEL_PATH)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_H)
    cap.set(cv2.CAP_PROP_FPS, REFRESH_RATE)

    scale_x = SCREEN_W / CAM_W
    scale_y = SCREEN_H / CAM_H

    start_t = time.perf_counter()
    next_frame_time = start_t
    running = True

    while running:
        now = time.perf_counter()
        if now < next_frame_time:
            time.sleep(next_frame_time - now)
        next_frame_time += FRAME_INTERVAL

        # ===== 摄像头读取 =====
        ret, frame = cap.read()
        if not ret:
            print("摄像头读取失败")
            break
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # YOLO 推理
        results = model(frame_rgb, classes=[0], verbose=False)
        centers = []
        if len(results) > 0 and hasattr(results[0], "boxes") and len(results[0].boxes) > 0:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            for box in boxes:
                x1, y1, x2, y2 = box.astype(int)
                cx = int((x1 + x2)/2 * scale_x)
                cy = int((y1 + y2)/2 * scale_y)
                centers.append((cx, cy))

        centers.sort(key=lambda c: c[0])
        centers = centers[:min(N_TARGETS, len(centers))]

        # resize 全屏
        frame_rgb_resized = cv2.resize(frame_rgb, (SCREEN_W, SCREEN_H), interpolation=cv2.INTER_LINEAR)
        frame_surface = pygame.image.frombuffer(frame_rgb_resized.tobytes(), (SCREEN_W, SCREEN_H), "RGB")
        screen.blit(frame_surface, (0, 0))

        # 当前时间，用于 SSVEP 正弦计算
        t = time.perf_counter() - start_t

        # 绘制多目标 SSVEP 刺激模块
        for idx, center in enumerate(centers):
            freq = STIM_FREQS[idx]
            phase = 2.0 * math.pi * freq * t
            intensity = (math.sin(phase)+1)/2
            lum = int(STIM_MIN_LUM + (STIM_MAX_LUM - STIM_MIN_LUM)*intensity)
            pygame.draw.circle(screen, (lum, lum, lum), center, STIM_RADIUS)

        pygame.display.flip()

        # 退出事件
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                running = False

    cap.release()
    pygame.mouse.set_visible(True)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
