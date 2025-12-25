#include "bird.h"
#include <QGraphicsScene>
Bird::Bird() : velocity(0), gravity(0.5), lift(-10), state(MidFlap) {
    setPixmap(QPixmap(":/assets/images/bluebird-midflap.png").scaled(40, 40));
    setPos(100, 300);
}

void Bird::flap() {
    velocity = lift;
    state = UpFlap;
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

    // 根据速度更新小鸟状态和图像
    if (velocity < -2) {  // 向上飞
        if (state != UpFlap) {
            state = UpFlap;
            updatePixmapForState();
        }
    } else if (velocity > 2) {  // 快速下降
        if (state != DownFlap) {
            state = DownFlap;
            updatePixmapForState();
        }
    } else {  // 平飞状态
        if (state != MidFlap) {
            state = MidFlap;
            updatePixmapForState();
        }
    }
}

void Bird::reset()
{
    state = MidFlap;
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
