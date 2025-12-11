#ifndef GAME_H
#define GAME_H

#include <QGraphicsView>
#include <QGraphicsScene>
#include <QTimer>
#include <QPushButton>
#include "bird.h"
#include "pipe.h"

class Game : public QGraphicsView {
	Q_OBJECT
public:
	Game(QWidget* parent = nullptr);
	void keyPressEvent(QKeyEvent* event);
	void restartGame();
signals:
	void gameOver();
private slots:
	void notifyGameOver();
	void gameLoop();

private:
	QGraphicsScene* scene;
	QGraphicsTextItem* scoreText;
	Bird* bird;
	QTimer* timer;
	QList<Pipe*> pipes;
	int score;
	bool isGameOver;
    QPushButton* menuButton;
};

#endif // GAME_H
