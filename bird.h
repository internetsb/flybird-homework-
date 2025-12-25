#ifndef BIRD_H
#define BIRD_H

#include <QGraphicsPixmapItem>
#include <QPixmap>

class Bird : public QGraphicsPixmapItem {
public:
    enum BirdState {
        MidFlap,
        UpFlap,
        DownFlap
    };

    Bird();
    void flap();
    void updatePosition();
    void reset();

private:
    qreal velocity;
    qreal gravity;
    qreal lift;
    BirdState state;
    void updatePixmapForState();
};

#endif // BIRD_H
