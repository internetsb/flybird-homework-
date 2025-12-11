#include <QApplication>
#include <QIcon>
#include "mainwindow.h"

int main(int argc, char* argv[]) {
    QApplication a(argc, argv);

    // 设置应用程序图标（资源路径）
    a.setWindowIcon(QIcon(":/assets/images/bluebird-upflap.png"));

    MainWindow w;
    w.show();

    return a.exec();
}
