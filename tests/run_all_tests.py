# run_all_tests.py（完全独立模式）

import subprocess
import sys
import time
import os
from datetime import datetime

# ==================== 配置区域 ====================
# 只需在这里配置一次，所有测试脚本会自动读取
os.environ[
    'GAME_EXE_PATH'] = r"C:\Users\zhanglei\Desktop\flybird-homework\build\Desktop_Qt_6_10_1_MinGW_64_bit-Debug\debug\flyBrid.exe"
os.environ['GAME_WINDOW_TITLE'] = "flyBrid"


# =================================================

def run_test_independent(script_name, description):
    """
    独立运行测试脚本
    - 每个脚本自己启动/关闭游戏
    - 避免进程间通信和句柄冲突
    """
    print(f"\n{'=' * 60}")
    print(f"开始执行: {description}")
    print(f"脚本: {script_name}")
    print(f"{'=' * 60}")

    try:
        # 直接执行，让测试脚本完全独立运行
        # 不捕获输出，避免任何编码或通信问题
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            stdout=None,  # 直接打印到控制台
            stderr=None,
            # 不需要传递任何复杂参数
        )

        print(f"✓ {description} 完成")
        return True

    except subprocess.CalledProcessError as e:
        print(f"✗ {description} 失败，退出码: {e.returncode}")
        return False
    except Exception as e:
        print(f"✗ {description} 异常: {e}")
        return False


def main():
    """主函数：顺序执行所有测试"""
    print("=" * 60)
    print("性能测试套件 - 完全独立模式")
    print("每个测试独立管理游戏生命周期")
    print("=" * 60)
    print(f"开始时间: {datetime.now()}")

    # 测试列表
    tests = [
        ("response_time_test.py", "1. 响应时间测试"),
        ("performance_monitor.py", "2. 性能监控测试"),
        ("stability_test.py", "3. 稳定性测试"),
    ]

    results = []
    for script, desc in tests:
        success = run_test_independent(script, desc)
        results.append((desc, success))

        # 测试间休息，确保资源释放
        if success:
            print("\n等待10秒后进行下一个测试...")
            time.sleep(10)

    # 打印总结报告
    print("\n" + "=" * 60)
    print("测试执行总结")
    print("=" * 60)
    print(f"结束时间: {datetime.now()}")

    all_passed = True
    for desc, success in results:
        status = "通过" if success else "失败"
        print(f"  {desc}: {status}")
        if not success:
            all_passed = False

    print(f"\n总体结果: {'所有测试通过' if all_passed else '部分测试失败'}")
    print("=" * 60)

    print("\n请查看生成的CSV日志文件获取详细数据")
    print("这些文件将用于填写测试报告")


if __name__ == "__main__":
    main()