# game_launcher.py
# 修复版：支持空格路径和健壮的错误处理

import subprocess
import time
import pyautogui
import psutil
import sys
import os


class GameLauncher:
    def __init__(self, game_exe_path, window_title, launch_timeout=30):
        # 关键修复：规范化路径
        self.game_exe_path = os.path.abspath(game_exe_path.strip())
        self.window_title = window_title.strip()
        self.launch_timeout = launch_timeout
        self.game_process = None

        print(f"-" * 50)
        print(f"初始化启动器:")
        print(f"  游戏路径: {self.game_exe_path}")
        print(f"  窗口标题: '{self.window_title}'")

        # 验证文件存在
        if not os.path.exists(self.game_exe_path):
            print(f"✗ 错误：游戏文件不存在！")
            sys.exit(1)
        print(f"  文件大小: {os.path.getsize(self.game_exe_path) / 1024 / 1024:.1f} MB")

    def is_game_running(self):
        """检查游戏窗口是否存在"""
        try:
            windows = pyautogui.getWindowsWithTitle(self.window_title)
            if windows:
                print(f"  → 检测到窗口: '{windows[0].title}'")
                return True
            return False
        except:
            return False

    def launch_game(self):
        """启动游戏：修复空格路径问题"""
        print(f"\n正在启动游戏...")

        # 关闭已运行的实例
        if self.is_game_running():
            print("  检测到游戏已在运行，先关闭...")
            self.terminate_game()
            time.sleep(3)  # 等待完全退出

        # 关键修复：Windows下使用字符串命令+shell=True
        try:
            if sys.platform == 'win32':
                # 用引号包裹路径，通过shell=True执行
                cmd = f'"{self.game_exe_path}"'
                print(f"  执行命令: {cmd}")
                self.game_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=True
                )
            else:
                self.game_process = subprocess.Popen(
                    [self.game_exe_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            print(f"  进程PID: {self.game_process.pid}")
            time.sleep(2)  # 等待进程初始化

            # 验证进程是否在运行
            if self.game_process.poll() is not None:
                print("✗ 错误：进程启动后立即退出！")
                sys.exit(1)

        except Exception as e:
            print(f"✗ 启动失败: {e}")
            sys.exit(1)

        # 等待窗口出现
        print(f"  等待窗口出现（{self.launch_timeout}秒超时）...")
        start_time = time.time()
        while time.time() - start_time < self.launch_timeout:
            if self.is_game_running():
                print("✓ 游戏窗口已加载！")
                time.sleep(2)
                return True
            time.sleep(1)

        print(f"✗ 超时：未检测到窗口 '{self.window_title}'")
        self.terminate_game()
        sys.exit(1)

    def get_game_window(self):
        """获取窗口对象"""
        windows = pyautogui.getWindowsWithTitle(self.window_title)
        if windows:
            return windows[0]
        raise Exception(f"未找到窗口 '{self.window_title}'")

    def activate_game(self):
        """激活窗口到前台"""
        window = self.get_game_window()
        try:
            if window.isMinimized:
                window.restore()
                time.sleep(0.5)
            window.activate()
            time.sleep(0.5)
            return window
        except:
            # 备用方案
            pyautogui.hotkey('alt', 'tab')
            time.sleep(1)
            return window

    def terminate_game(self):
        """终止游戏进程"""
        print("  正在关闭游戏...")
        killed = 0

        # 终止我们启动的进程
        if self.game_process:
            try:
                self.game_process.terminate()
                self.game_process.wait(timeout=10)
                print("  ✓ 主进程已终止")
            except:
                self.game_process.kill()

        # 强制终止所有匹配进程
        target = os.path.basename(self.game_exe_path).lower()
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if target in proc.info['name'].lower():
                    psutil.Process(proc.info['pid']).terminate()
                    killed += 1
            except:
                pass

        if killed > 0:
            print(f"  ✓ 清理了 {killed} 个残留进程")
        else:
            print("  ✓ 无残留进程")

        time.sleep(2)

    def __enter__(self):
        self.launch_game()
        return self

    def __exit__(self, *args):
        self.terminate_game()