import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI.main_ui import Ui_MainWindow  # 导入生成的界面类
from UI.extra_anime import Ui_AnimeBox
from UI.extra_publisher import Ui_PublisherBox
from UI.extra_platform import Ui_PlatformBox
from UI.extra_user import Ui_UserBox
from UI.extra_platformPurchase import Ui_PlatformPurchaseBox
from UI.extra_userFollow import Ui_UserFollowingBox
from PyQt5 import QtWidgets

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # 初始化界面

class Add(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_UserFollowingBox()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())