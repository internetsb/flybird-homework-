#include "mainwindow.h"
#include <QVBoxLayout>
#include <QPixmap>
#include <QLabel>

MainWindow::MainWindow(QWidget* parent)
    : QMainWindow(parent)
    , stack(nullptr)
    , startPage(nullptr)
    , creditsPage(nullptr)
    , gameView(nullptr)
{
    // 创建堆栈页面
    stack = new QStackedWidget(this);
    setCentralWidget(stack);

    // --- Start Page ---
    startPage = new QWidget(this);
    startPage->setFixedSize(400, 600);

    startBackground = new QLabel(startPage);
    QPixmap bg(":/assets/images/background-day.png");
    startBackground->setPixmap(bg.scaled(400, 600));
    startBackground->setFixedSize(400, 600);

    startButton = new QPushButton(tr("开始游戏"), startPage);
    creditsButton = new QPushButton(tr("制作人名单"), startPage);

    startButton->setGeometry(150, 380, 100, 40);
    creditsButton->setGeometry(150, 440, 100, 40);

    // 绿底白字样式
    QString greenStyle = "background-color: #2ecc71; color: white; border: none; border-radius: 6px; font-weight: bold;";
    startButton->setStyleSheet(greenStyle);
    creditsButton->setStyleSheet(greenStyle);

    stack->addWidget(startPage);

    // --- Credits Page ---
    creditsPage = new QWidget(this);
    creditsPage->setFixedSize(400, 600);
    QLabel* creditsLabel = new QLabel(creditsPage);
    creditsLabel->setWordWrap(true);
    creditsLabel->setText(tr("制作人:\n项目经理兼测试工程师：吴志凌\n桌面端开发工程师：章航恺\n资源设计师兼OOP架构师：张磊\n\n点击返回以返回开始界面"));
    creditsLabel->setGeometry(40, 100, 320, 300);
    creditsBackButton = new QPushButton(tr("返回"), creditsPage);
    creditsBackButton->setGeometry(150, 440, 100, 40);
    creditsBackButton->setStyleSheet("background-color: #2ecc71; color: white; border: none; border-radius: 6px; font-weight: bold;");
    stack->addWidget(creditsPage);

    // 连接按钮
    connect(startButton, &QPushButton::clicked, this, &MainWindow::startGame);
    connect(creditsButton, &QPushButton::clicked, this, &MainWindow::showCredits);
    connect(creditsBackButton, &QPushButton::clicked, [this]() { stack->setCurrentWidget(startPage); });

    // 显示开始页面
    stack->setCurrentWidget(startPage);

    // 固定主窗口大小与游戏视图一致
    setFixedSize(400, 600);
}

MainWindow::~MainWindow()
{
}

void MainWindow::startGame()
{
    // 如果已有游戏在运行，先清理
    if (gameView) {
        stack->removeWidget(gameView);
        delete gameView;
        gameView = nullptr;
    }

    gameView = new Game(this);
    // 将游戏视图加入堆栈并切换到游戏页面
    stack->addWidget(gameView);
    stack->setCurrentWidget(gameView);

    // 连接游戏结束信号，回到开始页面并销毁游戏视图
    connect(gameView, &Game::gameOver, this, &MainWindow::onGameOver);
}

void MainWindow::showCredits()
{
    stack->setCurrentWidget(creditsPage);
}

void MainWindow::onGameOver()
{
    if (!gameView) return;

    // 从堆栈移除并删除游戏视图
    stack->removeWidget(gameView);
    delete gameView;
    gameView = nullptr;

    // 返回开始页面
    stack->setCurrentWidget(startPage);
}
