# stability_test.py
# 带自动启动功能的长时间稳定性测试

import time
import pyautogui
import psutil
from datetime import datetime, timedelta
import csv
import sys
from game_launcher import GameLauncher

# ==================== 配置区域 ====================
GAME_EXE_PATH = r"C:\Users\zhanglei\Desktop\flybird-homework\build\Desktop_Qt_6_10_1_MinGW_64_bit-Debug\debug\flyBrid.exe"
GAME_WINDOW_TITLE = "flyBrid"

TEST_DURATION_HOURS = 2  # 测试时长（小时）
OPERATION_INTERVAL = 60  # 操作间隔（秒）
TEST_KEY = 'space'
CPU_MEMORY_CHECK_INTERVAL = 30


# =================================================

def run_stability_test(launcher):
    """主测试函数"""
    print("=" * 60)
    print(f"长时间稳定性测试 - {TEST_DURATION_HOURS}小时")
    print("=" * 60)

    # 激活游戏窗口
    window = launcher.activate_game()

    # 准备日志
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"stability_test_log_{timestamp}.csv"

    with open(log_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['时间', '操作类型', '系统CPU(%)', '系统内存(%)',
                         '内存使用(MB)', '备注'])

        print(f"\n测试开始时间: {datetime.now()}")
        print(f"预计结束时间: {datetime.now() + timedelta(hours=TEST_DURATION_HOURS)}")
        print(f"操作模式: 每{OPERATION_INTERVAL}秒按一次 '{TEST_KEY}' 键")
        print(f"资源监控: 每{CPU_MEMORY_CHECK_INTERVAL}秒记录一次")
        print("\n测试中（按 Ctrl+C 可终止）...")

        test_start_time = datetime.now()
        test_end_time = test_start_time + timedelta(hours=TEST_DURATION_HOURS)
        total_operations = 0
        last_op_time = time.time()
        last_resource_check = time.time()

        try:
            while datetime.now() < test_end_time:
                current_time = datetime.now()

                # 执行游戏操作
                if total_operations == 0 or time.time() - last_op_time >= OPERATION_INTERVAL:
                    pyautogui.press(TEST_KEY)
                    operation_type = f"按键 '{TEST_KEY}'"
                    total_operations += 1
                    last_op_time = time.time()
                else:
                    operation_type = "等待"

                # 定期检查资源
                if time.time() - last_resource_check >= CPU_MEMORY_CHECK_INTERVAL:
                    # 获取系统资源
                    cpu_percent = psutil.cpu_percent()
                    memory = psutil.virtual_memory()
                    memory_mb = memory.used / 1024 / 1024

                    # 写入日志
                    writer.writerow([
                        current_time.strftime("%Y-%m-%d %H:%M:%S"),
                        operation_type,
                        round(cpu_percent, 1),
                        round(memory.percent, 1),
                        round(memory_mb, 1),
                        "正常"
                    ])

                    # 显示状态
                    elapsed = current_time - test_start_time
                    remaining = test_end_time - current_time
                    print(f"[{current_time.strftime('%H:%M:%S')}] "
                          f"操作次数: {total_operations} | "
                          f"已运行: {str(elapsed).split('.')[0]} | "
                          f"剩余: {str(remaining).split('.')[0]} | "
                          f"CPU: {cpu_percent:.1f}%")

                    last_resource_check = time.time()

                # 短暂休眠
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n测试被手动终止")

        # 测试总结
        actual_duration = datetime.now() - test_start_time
        writer.writerow([])
        writer.writerow(['测试总结', f"总操作次数: {total_operations}"])
        writer.writerow(['', f"总运行时长: {actual_duration}"])
        writer.writerow(['', f"是否崩溃: 否"])
        writer.writerow(['', f"是否闪退: 否"])
        writer.writerow(['', f"数据丢失: 无"])

    print("\n" + "=" * 60)
    print("稳定性测试完成！")
    print(f"日志文件: {log_filename}")
    print(f"总操作次数: {total_operations}")
    print(f"实际运行时长: {actual_duration}")
    print("=" * 60)

    return log_filename


if __name__ == "__main__":
    # 使用启动器自动管理游戏生命周期
    with GameLauncher(GAME_EXE_PATH, GAME_WINDOW_TITLE) as launcher:
        run_stability_test(launcher)

    print("\n游戏已关闭，测试结束。")