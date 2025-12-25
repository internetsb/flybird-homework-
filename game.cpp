#include "game.h"
#include <QKeyEvent>
#include <QGraphicsTextItem>
#include <QIcon>
#include <QSettings>

Game::Game(QWidget* parent)
	: QGraphicsView(parent)
	, scene(nullptr)
	, scoreText(nullptr)
	, highScoreText(nullptr)
	, bird(nullptr)
	, timer(nullptr)
	, pipes()
	, score(0)
	, highScore(0)
	, isGameOver(false)
	, menuButton(nullptr)
{
	scene = new QGraphicsScene(this);
	setScene(scene);

    setWindowTitle("Ikun牌小鸟");

    QIcon icon(":/assets/images/bluebird-upflap.png");
    setWindowIcon(icon);

	bird = new Bird();
	scene->addItem(bird);

	// 定时器，控制游戏循环
	timer = new QTimer(this);
	connect(timer, &QTimer::timeout, this, &Game::gameLoop);
	timer->start(20);

	setFixedSize(400, 600);
	scene->setSceneRect(0, 0, 400, 600);

	scene->setBackgroundBrush(QBrush(QImage(":/assets/images/background-day.png").scaled(400, 600)));

	// 取消滚动条
	setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
	setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);

	// 创建并显示分数文本项
	scoreText = new QGraphicsTextItem(QString("Score: %1").arg(score));
	//放在最前面
	scoreText->setZValue(1);
	scoreText->setDefaultTextColor(Qt::white);
	scoreText->setFont(QFont("Arial", 20));
	scoreText->setPos(10, 10);
	scene->addItem(scoreText);

	// 读取并显示历史最高分
	QSettings settings("FlybirdCompany", "Flybird");
	highScore = settings.value("highScore", 0).toInt();
    highScoreText = new QGraphicsTextItem(QString::fromUtf8("Best: %1").arg(highScore));
	highScoreText->setZValue(1);
	highScoreText->setDefaultTextColor(Qt::white);
	highScoreText->setFont(QFont("Arial", 16));
	int hx = this->width() - highScoreText->boundingRect().width() - 10;
	highScoreText->setPos(hx, 14);
	scene->addItem(highScoreText);
}

void Game::keyPressEvent(QKeyEvent* event) {
	if (event->key() == Qt::Key_Space) {
		if (isGameOver) {
			restartGame();  // 如果游戏结束，按空格键重置游戏
			bird->flap();   // 在重新开始时也给小鸟一个向上加速度
		}
		else {
			bird->flap();  // 如果游戏在进行，按空格键让小鸟跳跃
		}
	}
}

void Game::restartGame()
{
	// 清除场景中的管道和文本
	for (Pipe* pipe : pipes) {
		scene->removeItem(pipe);
		delete pipe;
	}
	pipes.clear();

	// 重置小鸟的位置和状态
	bird->setPos(100, 300);
	bird->reset();

	// 重置分数
	score = 0;
	scoreText->setPlainText(QString("Score: %1").arg(score));

    // 移除 Game Over 画面
    QList<QGraphicsItem*> items = scene->items();
    for (QGraphicsItem* item : items) {
        if (QGraphicsPixmapItem* pixmapItem = dynamic_cast<QGraphicsPixmapItem*>(item))
        {
            if (pixmapItem->pixmap().cacheKey() == QPixmap(":/assets/images/gameover.png").cacheKey())
            {
                scene->removeItem(pixmapItem);
                delete pixmapItem;
            }
        }
        if (QGraphicsTextItem* textItem = dynamic_cast<QGraphicsTextItem*>(item)) {
            if (textItem->toPlainText() == "按空格键重新开始") {
                scene->removeItem(textItem);
                delete textItem;
            }
        }
    }

	// 重置游戏状态
	isGameOver = false;

	// 清理菜单按钮（若存在）
	if (menuButton) {
		menuButton->hide();
		delete menuButton;
		menuButton = nullptr;
	}

	timer->start(20);
}

void Game::gameLoop() {
	bird->updatePosition();

	// 生成新的管道
	if (pipes.isEmpty() || pipes.last()->x() < 200) {
		Pipe* pipe = new Pipe();
		pipes.append(pipe);
		scene->addItem(pipe);
	}

	// 管道移动与检测碰撞
	auto it = pipes.begin();
	while (it != pipes.end()) {
		Pipe* pipe = *it;
		pipe->movePipe();

		// 检测与小鸟的碰撞
		if (bird->collidesWithItem(pipe)) {
			timer->stop();
			QGraphicsPixmapItem* gameOverItem = scene->addPixmap(QPixmap(":/assets/images/gameover.png"));
			// 将 Game Over 画面放在背景上方中部（靠近顶部）
			int gx = this->width() / 2 - gameOverItem->pixmap().width() / 2;
            int gy = this->height() / 2 - gameOverItem->pixmap().height() / 2;
			gameOverItem->setPos(gx, gy);
			isGameOver = true;
			// 提示按空格重新开始，放在 gameover 图片下方
			QGraphicsTextItem* restartText = new QGraphicsTextItem("按空格键重新开始");
			restartText->setDefaultTextColor(Qt::black);
			restartText->setFont(QFont("Arial", 12, QFont::Bold));
			restartText->setPos(this->width() / 2 - restartText->boundingRect().width() / 2, gy + gameOverItem->pixmap().height() + 10);
			scene->addItem(restartText);

			// 创建一个与主界面样式一致的“返回主菜单”按钮（如果尚未创建）
			if (!menuButton) {
				menuButton = new QPushButton(tr("返回主菜单"), this);
				QString greenStyle = "background-color: #2ecc71; color: white; border: none; border-radius: 6px; font-weight: bold;";
				menuButton->setStyleSheet(greenStyle);
				int bw = 140;
				int bh = 36;
				int bx = this->width() / 2 - bw / 2;
				int by = gy + gameOverItem->pixmap().height() + 40;
				menuButton->setGeometry(bx, by, bw, bh);
				menuButton->show();
				connect(menuButton, &QPushButton::clicked, this, &Game::notifyGameOver);
			}

			// 不立即通知外部，保留 Game Over 显示，等待玩家操作（空格重启 或 点击返回主菜单）

			// 保存最高分到设置
			QSettings settings("FlybirdCompany", "Flybird");
			settings.setValue("highScore", highScore);
			return;
		}

		// 如果小鸟通过了管道（即小鸟的x坐标刚好超过管道的x坐标）
		if (pipe->x() + pipe->boundingRect().width() < bird->x() && !pipe->isPassed) {
			// 增加分数
			score++;
			pipe->isPassed = true;  // 确保不会重复加分

			// 更新分数显示
			scoreText->setPlainText(QString("Score: %1").arg(score));

			// 如果当前分数超过历史最高分，更新显示（保存在游戏结束时完成）
			if (score > highScore) {
				highScore = score;
				if (highScoreText) {
					highScoreText->setPlainText(QString::fromUtf8("最高分: %1").arg(highScore));
					int hx = this->width() - highScoreText->boundingRect().width() - 10;
					highScoreText->setPos(hx, 14);
				}
			}
		}

		// 如果管道移出了屏幕，将其从场景和列表中删除
		if (pipe->x() < -60) {
			scene->removeItem(pipe);
			delete pipe;
			it = pipes.erase(it);  // 从列表中安全移除管道
		}
		else {
			++it;  // 继续遍历
		}
	}
}

void Game::notifyGameOver()
{
	emit gameOver();
}
