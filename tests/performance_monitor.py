# performance_monitor.py
# 带自动启动功能的性能监控脚本

import time
import psutil
import csv
from datetime import datetime
import sys
from game_launcher import GameLauncher

# ==================== 配置区域 ====================
GAME_EXE_PATH = r"C:\Users\zhanglei\Desktop\flybird-homework\build\Desktop_Qt_6_10_1_MinGW_64_bit-Debug\debug\flyBrid.exe"
GAME_WINDOW_TITLE = "flyBrid"

MONITOR_DURATION = 1800  # 监控时长（30分钟）
SAMPLE_INTERVAL = 1
CPU_WARNING_THRESHOLD = 50
MEMORY_WARNING_THRESHOLD = 500


# =================================================

def get_game_pid_by_title(launcher):
    """通过窗口标题查找游戏进程PID"""
    try:
        window = launcher.get_game_window()
        # 找到窗口后，查找对应的进程
        for proc in psutil.process_iter(['pid', 'name']):
            if GAME_WINDOW_TITLE.lower() in proc.info['name'].lower():
                return proc.info['pid']
        raise Exception("未找到游戏进程")
    except Exception as e:
        print(f"获取进程PID失败: {e}")
        sys.exit(1)


def get_frame_rate():
    """
    获取游戏帧率 - 需要根据你的游戏实现
    方案A（推荐）：游戏输出FPS到日志文件
    方案B：使用PresentMon等外部工具
    方案C：从游戏内存读取（高级）
    """
    # 临时方案：返回模拟数据
    # TODO: 实现真实FPS采集
    return 60


def monitor_performance(launcher):
    """主监控函数"""
    print("=" * 50)
    print("性能监控测试")
    print("=" * 50)

    # 激活游戏窗口
    launcher.activate_game()

    # 获取游戏进程
    pid = get_game_pid_by_title(launcher)
    process = psutil.Process(pid)
    print(f"已连接到进程 PID: {pid}")

    # 准备日志文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"performance_log_{timestamp}.csv"

    with open(log_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['时间戳', '帧率(FPS)', 'CPU使用率(%)', '内存使用(MB)',
                         '内存使用(%)', '告警信息'])

        print(f"\n开始监控（预计{MONITOR_DURATION}秒）...")
        print("实时监控中（按 Ctrl+C 可提前终止）...")

        start_time = time.time()
        sample_count = 0
        frame_rates = []
        cpu_usages = []
        memory_usages = []

        try:
            while time.time() - start_time < MONITOR_DURATION:
                loop_start = time.time()

                # 采集数据
                current_time = datetime.now().strftime("%H:%M:%S")
                fps = get_frame_rate()
                cpu_percent = process.cpu_percent()
                memory_info = process.memory_info()
                memory_mb = memory_info.rss / 1024 / 1024
                memory_percent = process.memory_percent()

                # 统计
                frame_rates.append(fps)
                cpu_usages.append(cpu_percent)
                memory_usages.append(memory_mb)
                sample_count += 1

                # 检查告警
                warning = ""
                if cpu_percent > CPU_WARNING_THRESHOLD:
                    warning += f"CPU过高({cpu_percent:.1f}%) "
                if memory_mb > MEMORY_WARNING_THRESHOLD:
                    warning += f"内存过高({memory_mb:.1f}MB) "

                # 写入日志
                writer.writerow([
                    current_time, fps,
                    round(cpu_percent, 1),
                    round(memory_mb, 1),
                    round(memory_percent, 1),
                    warning
                ])

                # 实时显示
                if sample_count % 10 == 0:
                    elapsed = int(time.time() - start_time)
                    remaining = MONITOR_DURATION - elapsed
                    print(f"[{current_time}] 进度:{elapsed}/{MONITOR_DURATION}s "
                          f"FPS:{fps} CPU:{cpu_percent:.1f}% "
                          f"内存:{memory_mb:.1f}MB {warning}")

                # 控制采样频率
                elapsed = time.time() - loop_start
                if elapsed < SAMPLE_INTERVAL:
                    time.sleep(SAMPLE_INTERVAL - elapsed)

        except KeyboardInterrupt:
            print("\n\n监控被手动终止")

        # 统计摘要
        writer.writerow([])
        writer.writerow(['统计项', '平均值', '峰值', '最低值'])
        writer.writerow([
            '帧率(FPS)',
            round(sum(frame_rates) / len(frame_rates), 1),
            round(max(frame_rates), 1),
            round(min(frame_rates), 1)
        ])
        writer.writerow([
            'CPU使用率(%)',
            round(sum(cpu_usages) / len(cpu_usages), 1),
            round(max(cpu_usages), 1),
            round(min(cpu_usages), 1)
        ])
        writer.writerow([
            '内存使用(MB)',
            round(sum(memory_usages) / len(memory_usages), 1),
            round(max(memory_usages), 1),
            round(min(memory_usages), 1)
        ])

    print("\n" + "=" * 50)
    print("监控完成！")
    print(f"数据已保存至: {log_filename}")
    print(f"总采样点数: {sample_count}")
    print("=" * 50)

    return log_filename


if __name__ == "__main__":
    # 使用启动器自动管理游戏
    with GameLauncher(GAME_EXE_PATH, GAME_WINDOW_TITLE) as launcher:
        monitor_performance(launcher)

    print("\n游戏已关闭，测试结束。")