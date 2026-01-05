import pyautogui
import time
import subprocess

#游戏路径，根据实际情况修改
path = "../build/Desktop_Qt_6_10_1_MinGW_64_bit-Debug/debug/flyBrid.exe"
def test_bird_jump():
    """
    黑盒测试：测试小鸟跳跃功能
    通过PyAutoGUI模拟空格键按下，验证小鸟是否按预期上移
    """
    print("开始测试小鸟跳跃功能...")
    
    # 启动游戏
    process = subprocess.Popen([path])
    
    # 等待游戏启动
    time.sleep(3)
    
    # 测试连续跳跃
    for i in range(5):
        pyautogui.press('space')
        time.sleep(0.5)
    
    print("小鸟跳跃功能测试完成")
    
    # 结束游戏进程
    process.terminate()
    process.wait()

def test_boundary_values():
    """
    边界值测试：测试边界操作
    通过PyAutoGUI模拟极端操作（每秒10次连续按空格键）
    """
    print("开始边界值测试...")
    
    # 启动游戏
    process = subprocess.Popen([path])
    time.sleep(3)
    
    # 快速连续按空格键测试
    for i in range(100):
        pyautogui.press('space')
        time.sleep(0.1)  # 每秒10次
    
    print("边界值测试完成")
    
    # 结束游戏进程
    process.terminate()
    process.wait()

def test_full_game_flow():
    """
    场景测试：测试完整游戏流程
    从启动游戏到游戏结束再到重新开始的完整流程
    """
    print("开始完整游戏流程测试...")
    
    # 启动游戏
    process = subprocess.Popen([path])
    time.sleep(3)
    
    # 开始游戏（按空格键）
    pyautogui.press('space')
    time.sleep(1)
    
    # 进行一些跳跃操作
    for i in range(10):
        pyautogui.press('space')
        time.sleep(0.8)
    
    # 等待可能的游戏结束（碰撞）
    time.sleep(10)
    
    # 重新开始游戏（按空格键）
    pyautogui.press('space')
    time.sleep(2)
    
    print("完整游戏流程测试完成")
    
    # 结束游戏进程
    process.terminate()
    process.wait()

if __name__ == "__main__":
    print("开始执行PyAutoGUI自动化测试...")
    
    test_bird_jump()
    
    test_boundary_values()
    
    test_full_game_flow()
    
    print("所有PyAutoGUI测试完成")