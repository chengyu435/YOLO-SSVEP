# ssvep_6hz.py
import sys
import math
import time
import pygame
import ctypes


# 仅在 Windows 下设置真实 DPI 感知
if sys.platform == "win32":
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception as e:
        print("DPI awareness 设置失败：", e)
# ---------- 配置参数 ----------
SCREEN_W = 2560
SCREEN_H = 1440
REFRESH_RATE = 60.0   # 你提供的刷新率（Hz），用于帧率限制/参考（实际频率以显示器为准）
FREQ_HZ = 6.0          # 刺激频率（Hz）
STIM_RADIUS = 100      # 刺激半径（像素），按需要调整
STIM_MAX_LUM = 255     # 亮度最大值
STIM_MIN_LUM = 0       # 亮度最小值
BG_COLOR = (0, 0, 0)   # 黑色背景
CENTER = (SCREEN_W // 2, SCREEN_H // 2)
# -------------------------------

def try_set_mode(size):
    """尝试以 vsync 模式全屏打开（若 pygame 支持），否则退回到普通全屏。"""
    flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
    try:
        # pygame 2 可以接受 vsync 参数
        screen = pygame.display.set_mode(size, flags, vsync=1)
    except TypeError:
        # 如果不支持 vsync 参数，调用不带参数的 set_mode
        screen = pygame.display.set_mode(size, flags)
    return screen

def main():
    pygame.init()
    pygame.display.set_caption("SSVEP 6Hz Stimulus (ESC to quit)")

    # 尝试设置目标分辨率（若系统不支持则自动回退）
    try:
        screen = try_set_mode((SCREEN_W, SCREEN_H))
    except Exception as e:
        print("无法以指定分辨率全屏打开，尝试窗口模式。错误：", e)
        screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    # 隐藏鼠标
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()

    start_t = time.perf_counter()

    running = True
    while running:
        # 事件处理
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False

        # 计算当前时间和相位（使用高精度计时）
        t = time.perf_counter() - start_t
        phase = 2.0 * math.pi * FREQ_HZ * t
        # 正弦在 -1..1 -> 映射到 0..1，然后映射到亮度
        intensity = (math.sin(phase) + 1.0) / 2.0
        lum = int(STIM_MIN_LUM + (STIM_MAX_LUM - STIM_MIN_LUM) * intensity)
        color = (lum, lum, lum)

        # 绘制
        screen.fill(BG_COLOR)
        # 在中心绘制一个填充圆，亮度由正弦调制
        pygame.draw.circle(screen, color, CENTER, STIM_RADIUS)

        # 更新显示（使用双缓冲）
        pygame.display.flip()

        # 限制帧率到接近显示器刷新率（尽量让每帧与垂直同步对齐）
        # 如果启用了 vsync，flip() 本身会阻塞到垂直刷新；这里仅作限制参考
        clock.tick(REFRESH_RATE)

    # 退出清理
    pygame.mouse.set_visible(True)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
