# response_time_test.py
# 带自动启动功能的响应时间测试脚本

import time
import pyautogui
import csv
from datetime import datetime
import sys
from game_launcher import GameLauncher  # 导入启动器

# ==================== 配置区域 ====================
# 只需修改这两个参数！
GAME_EXE_PATH = r"C:\Users\zhanglei\Desktop\flybird-homework\build\Desktop_Qt_6_10_1_MinGW_64_bit-Debug\debug\flyBrid.exe"
GAME_WINDOW_TITLE = "flyBrid"  # 你的游戏窗口标题

# 测试参数
TEST_KEY = 'space'  # 测试按键
TOTAL_TESTS = 100
RESPONSE_TIME_LIMIT = 50  # 响应时间标准（毫秒）
FEEDBACK_PIXEL_X = 500  # 游戏反馈检测点X坐标（相对于窗口）
FEEDBACK_PIXEL_Y = 300  # 游戏反馈检测点Y坐标


# =================================================

def get_relative_position(window, relative_x, relative_y):
    """将相对坐标转换为屏幕绝对坐标"""
    return window.left + relative_x, window.top + relative_y


def detect_feedback_by_color(window, screen_x, screen_y):
    """检测指定位置颜色变化"""
    # 获取操作前颜色
    try:
        before_color = pyautogui.pixel(screen_x, screen_y)
    except Exception as e:
        print(f"无法获取初始颜色: {e}")
        return False, time.perf_counter()

    # 持续监测颜色变化（最多等待100ms）
    start_wait = time.perf_counter()
    while (time.perf_counter() - start_wait) < 0.1:
        try:
            current_color = pyautogui.pixel(screen_x, screen_y)
            if current_color != before_color:
                return True, time.perf_counter()
        except Exception as e:
            print(f"颜色检测错误: {e}")
            return False, time.perf_counter()
        time.sleep(0.001)

    return False, time.perf_counter()


def run_response_time_test(launcher):
    """主测试函数"""
    print("=" * 50)
    print("游戏操作响应时间测试")
    print("=" * 50)

    # 激活游戏窗口
    window = launcher.activate_game()

    # 计算屏幕绝对坐标
    screen_x, screen_y = get_relative_position(window, FEEDBACK_PIXEL_X, FEEDBACK_PIXEL_Y)
    print(f"检测点坐标（屏幕绝对）: ({screen_x}, {screen_y})")

    # 准备日志文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"response_time_log_{timestamp}.csv"

    with open(log_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['测试序号', '操作时间戳', '反馈时间戳', '响应时间(ms)', '是否达标'])

        # 预热测试（不计入结果）
        print(f"\n执行5次预热测试...")
        for _ in range(5):
            pyautogui.press(TEST_KEY)
            time.sleep(0.1)

        # 正式测试
        print(f"开始{TOTAL_TESTS}次正式测试...")
        response_times = []
        success_count = 0

        for i in range(1, TOTAL_TESTS + 1):
            # 随机间隔模拟真实玩家（0.5-1.5秒）
            time.sleep(0.5 + 0.5 * (i % 3))

            # 记录操作开始时间（高精度）
            press_time = time.perf_counter()
            pyautogui.press(TEST_KEY)

            # 检测游戏反馈
            feedback_detected, feedback_time = detect_feedback_by_color(
                window, screen_x, screen_y)

            # 计算响应时间
            response_time_ms = (feedback_time - press_time) * 1000

            # 判定是否达标
            is_pass = feedback_detected and response_time_ms < RESPONSE_TIME_LIMIT

            # 记录数据
            writer.writerow([i, press_time, feedback_time,
                             round(response_time_ms, 2),
                             "是" if is_pass else "否"])

            response_times.append(response_time_ms)
            if is_pass:
                success_count += 1

            # 实时显示进度
            status = "✓" if is_pass else "✗"
            print(f"  测试 {i}/{TOTAL_TESTS}: {response_time_ms:.2f}ms {status}")

        # 计算统计数据
        avg_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        success_rate = (success_count / TOTAL_TESTS) * 100

        # 写入统计摘要
        writer.writerow([])
        writer.writerow(['统计项', '数值'])
        writer.writerow(['平均响应时间(ms)', round(avg_time, 2)])
        writer.writerow(['最小响应时间(ms)', round(min_time, 2)])
        writer.writerow(['最大响应时间(ms)', round(max_time, 2)])
        writer.writerow(['成功率(%)', round(success_rate, 2)])

    # 打印最终报告
    print("\n" + "=" * 50)
    print("测试完成！")
    print(f"数据已保存至: {log_filename}")
    print(f"平均响应时间: {avg_time:.2f} ms")
    print(f"是否满足 < {RESPONSE_TIME_LIMIT}ms 标准: {'是' if avg_time < RESPONSE_TIME_LIMIT else '否'}")
    print(f"成功率: {success_rate:.1f}%")
    print("=" * 50)

    return log_filename


if __name__ == "__main__":
    # 安全模式：移动鼠标到左上角可终止
    pyautogui.FAILSAFE = True

    # 使用启动器自动管理游戏生命周期
    with GameLauncher(GAME_EXE_PATH, GAME_WINDOW_TITLE) as launcher:
        # 在游戏运行时执行测试
        run_response_time_test(launcher)

    # 游戏会自动关闭
    print("\n游戏已关闭，测试结束。")