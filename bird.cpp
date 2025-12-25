#include "bird.h"
#include <QGraphicsScene>
Bird::Bird() : velocity(0), gravity(0.5), lift(-10), state(MidFlap), flapAnimationTimer(0) {
	setPixmap(QPixmap(":/assets/images/bluebird-midflap.png").scaled(40, 40));
	setPos(100, 300);
}

void Bird::flap() {
	velocity = lift;
	state = UpFlap;
	flapAnimationTimer = 8;  // 设置flap动画持续时间
	updatePixmapForState();
}

void Bird::updatePosition() {
	velocity += gravity;
	setY(y() + velocity);

	// 限制鸟的活动范围
	if (y() < 0) {
		setY(0);
		velocity = 0;
	}
	else if (y() > 560) {
		setY(560);
		velocity = 0;
	}

	// 更新flap动画计时器
	if (flapAnimationTimer > 0) {
		flapAnimationTimer--;
		if (flapAnimationTimer == 0 && state != DownFlap) {
			// flap动画结束后，根据速度决定状态
			if (velocity > 2) {
				state = DownFlap;
				updatePixmapForState();
			} else {
				state = MidFlap;
				updatePixmapForState();
			}
		}
	} else if (velocity > 2 && state != DownFlap) {
		// 只有在下降时才显示下降图像
		state = DownFlap;
		updatePixmapForState();
	}

	// 每帧减少计时器
	if (flapAnimationTimer > 0) {
		flapAnimationTimer--;
	}
}

void Bird::reset()
{
	state = MidFlap;
	flapAnimationTimer = 0;
	updatePixmapForState();
	setPos(100, 300);
}

void Bird::updatePixmapForState() {
    QString imagePath;
    switch (state) {
        case UpFlap:
            imagePath = ":/assets/images/bluebird-upflap.png";
            break;
        case DownFlap:
            imagePath = ":/assets/images/bluebird-downflap.png";
            break;
        case MidFlap:
        default:
            imagePath = ":/assets/images/bluebird-midflap.png";
            break;
    }
    setPixmap(QPixmap(imagePath).scaled(40, 40));
}