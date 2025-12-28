# 飞鸟游戏 (Fly Bird)

## 项目概述

飞鸟游戏 (Fly Bird) 是一款基于 Qt 框架开发的 C++ 游戏应用，灵感来源于经典游戏《Flappy Bird》。玩家控制一只小鸟穿过管道障碍，体验重力模拟和反应速度挑战。

### 演示视频

观看我们的演示，了解游戏的实际运行效果：

![演示](./Document/演示.gif)

该视频展示了游戏的完整游玩过程，包括：

- 游戏开始界面
- 小鸟控制和重力模拟
- 管道障碍物的移动
- 分数统计

## 技术栈

- **编程语言**: C++
- **框架**: Qt 6.9.2
- **构建系统**: CMake
- **编译器**: MinGW 64-bit

## 功能特性

- 小鸟的飞行与重力模拟
- 管道障碍物的生成与移动
- 游戏主循环与碰撞检测
- Qt 图形界面渲染
- 分数统计与最高分记录

## 团队协作

### 开发流程

1. **需求分析**: 确定核心游戏机制和用户界面
2. **架构设计**: 分离游戏逻辑与界面展示，采用 MVC 模式
3. **模块开发**:
   - [Bird](./bird.h) 类负责小鸟的物理模拟和动画
   - [Pipe](./pipe.h) 类处理障碍物的生成与移动
   - [Game](./game.h) 类管理游戏循环和状态
   - [MainWindow](./mainwindow.h) 类提供主界面和菜单系统
4. **集成测试**: 合并各模块并进行整体测试
5. **优化迭代**: 根据测试结果优化性能和用户体验

### 版本控制

- 使用 Git 进行版本控制

### 协作工具

- **IDE**: Qt Creator
- **版本控制**: Git
- **项目管理**: GitHub

## 演示说明

### 环境准备

1. 安装 Qt 6.9.2 (带 MinGW 64-bit)
2. 配置环境变量包含 qmake 和 cmake
3. 安装 CMake 3.30.5

### 构建与运行

#### 方法一：使用 Qt Creator

1. 打开项目文件夹
2. Qt Creator 会自动识别 CMakeLists.txt
3. 点击"构建"按钮
4. 点击"运行"按钮启动游戏

#### 方法二：命令行构建

```bash
# 进入项目目录
cd d:\IE\MyProject\flybird-homework-

# 创建构建目录
mkdir build && cd build

# 配置项目
cmake ..

# 编译项目
cmake --build .
```

### 游戏操作

- **空格键**: 控制小鸟跳跃
- **重启游戏**: 游戏结束后点击菜单按钮重新开始
- **主菜单**: 游戏结束后可返回主菜单

### 演示要点

1. **游戏机制演示**:
   - 展示小鸟的重力效果
   - 演示管道随机生成与移动
   - 展示碰撞检测机制
2. **界面功能演示**:
   - 主菜单界面展示
   - 游戏界面操作
   - 结束界面与分数显示
3. **技术特性演示**:
   - Qt 信号与槽机制
   - QTimer 驱动的游戏循环

## 项目结构

```
flybird-homework-/
├── flybird/                 # Qt 项目目录
│   ├── main.cpp             # 程序入口
│   ├── mainwindow.cpp/h     # 主窗口实现
│   ├── flybird_zh_CN.ts     # 中文翻译文件
│   └── build/               # 构建输出目录
├── bird.cpp/h               # 小鸟类定义与实现
├── pipe.cpp/h               # 管道类定义与实现
├── game.cpp/h               # 游戏主逻辑
├── mainwindow.cpp/h         # 主窗口实现
├── Document/                # 文档目录
│   ├── FLYBIRD_需求规格说明书.doc
│   ├── FLYBIRD_面向对象分析文档.doc
│   ├── FLYBIRD_面向对象设计文档.docx
│   ├── UML类图.png
│   ├── 时序图-启动流程.png
│   ├── 时序图-游戏.png
│   ├── 时序图-计分.png
│   ├── 演示                   # 演示视频文件
│   └── 用例图.png
├── assets/                  # 资源文件目录
└── README.md                # 项目说明文档
```

## 当前状态与未来工作

### 已实现功能

- 完整的游戏核心机制
- 图形用户界面
- 分数统计系统

### 待完成工作

- [x] UML 类图设计文档
- [x] 单元测试覆盖
- [ ] 性能优化
- [ ] 更多游戏特性 (如音效、动画效果)

## 贡献者

- [吴志凌]
- [张磊]
- [章航恺]
- [吴雪灵]

## 许可证

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
