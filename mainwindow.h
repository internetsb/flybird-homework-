#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QStackedWidget>
#include <QPushButton>
#include <QLabel>
#include "game.h"

class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    MainWindow(QWidget* parent = nullptr);
    ~MainWindow();
private slots:
    void startGame();
    void showCredits();
    void onGameOver();
private:
    QStackedWidget* stack;
    QWidget* startPage;
    QWidget* creditsPage;
    Game* gameView;
    QPushButton* startButton;
    QPushButton* creditsButton;
    QPushButton* creditsBackButton;
    QLabel* startBackground;
};

#endif // MAINWINDOW_H
