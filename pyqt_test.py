import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


class Example(QWidget):            #定义Example继承QWidget

                                   #super()方法返回了Example类的父类对象，并且我们调用了父类的构造方法。
    def __init__(self):            #def __init__(self, parent=None)   #也可以这样写
        super().__init__()         #super(Example, self).__init__(parent)

        self.my_UI()              #GUI的创建授予my_UI()方法完成。


    def my_UI(self):              #这些方法都是继承自QWidget类

        self.setGeometry(300, 300, 300, 220) #setGeometry()做了两件事：将窗口在屏幕上显示，并设置了它的尺寸。setGeometry()方法的前两个参数定位了窗口的x轴和y轴位置。第三个参数是定义窗口的宽度，第四个参数是定义窗口的高度。
        #self.move(300, 300)                 #等于将resize()和move()方法融合在一个方法内
        #self.resize(300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('icon.png'))

        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()                          #创建实例
    sys.exit(app.exec_())