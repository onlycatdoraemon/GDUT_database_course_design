import os

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        self.background = "./picture/background.jpg"

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 800)  # 初始窗口大小
        MainWindow.setWindowTitle("番剧数据库管理系统")
        MainWindow.setWindowIcon(QtGui.QIcon("./picture/icon_1.png"))
        MainWindow.setStyleSheet("QWidget {background-color: rgb(255, 255, 255);}")

        # 主窗口的中央 widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 创建主布局（垂直布局）
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(10, 10, 10, 10)  # 设置主窗口边距
        main_layout.setSpacing(10)  # 控件之间的间距

        # Tab Widget：用于切换不同的管理模块
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)  # 自动适配窗口大小

        # 出版社管理 Tab
        self.publisher_tab = QtWidgets.QWidget()
        self.publisher_tab.setObjectName("publisher_tab")
        self.setupPublisherTab(self.publisher_tab)
        self.tabWidget.addTab(self.publisher_tab, "出版社管理")

        # 番剧管理 Tab
        self.anime_tab = QtWidgets.QWidget()
        self.anime_tab.setObjectName("anime_tab")
        self.setupAnimeTab(self.anime_tab)
        self.tabWidget.addTab(self.anime_tab, "番剧管理")

        # 平台管理 Tab
        self.platform_tab = QtWidgets.QWidget()
        self.platform_tab.setObjectName("platform_tab")
        self.setupPlatformTab(self.platform_tab)
        self.tabWidget.addTab(self.platform_tab, "平台管理")
        # 用户管理 Tab
        self.user_tab = QtWidgets.QWidget()
        self.user_tab.setObjectName("user_tab")
        self.setupUserTab(self.user_tab)
        self.tabWidget.addTab(self.user_tab, "用户管理")

        # 购入番剧管理 Tab
        self.PlatformPurchase_tab = QtWidgets.QWidget()
        self.PlatformPurchase_tab.setObjectName("PlatformPurchase_tab")
        self.setupPlatformPurchaseTab(self.PlatformPurchase_tab)
        self.tabWidget.addTab(self.PlatformPurchase_tab, "购入番剧管理")
        # 用户追番管理 Tab
        self.UserFollowing_tab = QtWidgets.QWidget()
        self.UserFollowing_tab.setObjectName("UserFollowing_tab")
        self.setupUserFollowingTab(self.UserFollowing_tab)
        self.tabWidget.addTab(self.UserFollowing_tab, "用户追番管理")

        # 额外功能
        self.extra_tab = QtWidgets.QWidget()
        self.extra_tab.setObjectName("extra_tab")
        self.setupExtraTab(self.extra_tab)
        self.tabWidget.addTab(self.extra_tab, "额外功能")

        # 添加 tabWidget 到主布局
        main_layout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        # 状态栏
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        # 设置窗口大小策略，支持动态调整
        MainWindow.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def setupPublisherTab(self, tab):
        """设置出版社管理界面"""
        # 创建主布局：垂直布局
        main_layout = QtWidgets.QVBoxLayout(tab)  # 主布局管理整个 tab 页
        main_layout.setContentsMargins(10, 10, 10, 10)  # 设置四周的边距
        main_layout.setSpacing(10)  # 控件之间的间距

        # 搜索框整体框架（水平布局）
        self.search_frame_publisher = QtWidgets.QFrame()
        self.search_frame_publisher.setObjectName("search_frame_publisher")
        search_layout = QtWidgets.QHBoxLayout(self.search_frame_publisher)  # 水平布局管理搜索框
        search_layout.setContentsMargins(0, 0, 0, 0)  # 搜索框的边距
        search_layout.setSpacing(10)  # 搜索框内部控件间距

        # 搜索输入框
        self.search_edit_publisher = QtWidgets.QLineEdit()
        self.search_edit_publisher.setPlaceholderText("搜索出版社信息（支持模糊搜索by名字）")
        self.search_edit_publisher.setObjectName("search_edit_publisher")
        search_layout.addWidget(self.search_edit_publisher)  # 添加到布局

        # 搜索按钮
        self.search_button_publisher = QtWidgets.QPushButton("搜索")
        self.search_button_publisher.setObjectName("search_button_publisher")
        search_layout.addWidget(self.search_button_publisher)  # 添加到布局

        # 添加出版社按钮
        self.add_button_publisher = QtWidgets.QPushButton("添加出版社")
        self.add_button_publisher.setObjectName("add_button_publisher")
        search_layout.addWidget(self.add_button_publisher)  # 添加到布局

        # 删除出版社按钮
        self.delete_button_publisher = QtWidgets.QPushButton("删除出版社")
        self.delete_button_publisher.setObjectName("delete_button_publisher")
        search_layout.addWidget(self.delete_button_publisher)  # 添加到布局

        # 更改出版社按钮
        self.change_button_publisher = QtWidgets.QPushButton("更改出版社")
        self.change_button_publisher.setObjectName("change_button_publisher")
        search_layout.addWidget(self.change_button_publisher)  # 添加到布局

        main_layout.addWidget(self.search_frame_publisher)  # 搜索框添加到主布局

        # 表格：出版社信息展示表格
        self.publisher_table = QtWidgets.QTableWidget()
        self.publisher_table.setObjectName("publisher_table")
        self.publisher_table.setColumnCount(3)  # 示例列数
        self.publisher_table.setHorizontalHeaderLabels(["出版社ID", "名称", "制作番剧数量"])
        self.publisher_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.publisher_table.setStyleSheet(
            f"QWidget {{background-image: url({self.background});"
            f" background-repeat: no-repeat;"
            f" background-position: center;"
            f" background-size: cover;}}")
        self.publisher_table.verticalHeader().setVisible(False)  # 隐藏行号
        # 设置垂直滚动条总是显示
        self.publisher_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # 设置水平滚动条根据需要显示
        self.publisher_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        main_layout.addWidget(self.publisher_table)  # 表格添加到主布局

    def setupAnimeTab(self, tab):
        """设置番剧管理界面"""
        # 创建主布局：垂直布局
        main_layout = QtWidgets.QVBoxLayout(tab)  # 主布局管理整个 tab 页
        main_layout.setContentsMargins(10, 10, 10, 10)  # 设置四周的边距
        main_layout.setSpacing(10)  # 控件之间的间距

        # 搜索框整体框架（水平布局）
        self.search_frame_anime = QtWidgets.QFrame()
        self.search_frame_anime.setObjectName("search_frame_anime")
        search_layout = QtWidgets.QHBoxLayout(self.search_frame_anime)  # 水平布局管理搜索框
        search_layout.setContentsMargins(0, 0, 0, 0)  # 搜索框的边距
        search_layout.setSpacing(10)  # 搜索框内部控件间距

        # 搜索输入框
        self.search_edit_anime = QtWidgets.QLineEdit()
        self.search_edit_anime.setPlaceholderText("搜索番剧信息（支持模糊搜索by名字）")
        self.search_edit_anime.setObjectName("search_edit_anime")
        search_layout.addWidget(self.search_edit_anime)  # 添加到布局

        # 搜索按钮
        self.search_button_anime = QtWidgets.QPushButton("搜索")
        self.search_button_anime.setObjectName("search_button_anime")
        search_layout.addWidget(self.search_button_anime)  # 添加到布局

        # 添加番剧按钮
        self.add_button_anime = QtWidgets.QPushButton("添加番剧")
        self.add_button_anime.setObjectName("add_button_anime")
        search_layout.addWidget(self.add_button_anime)  # 添加到布局

        # 删除番剧按钮
        self.delete_button_anime = QtWidgets.QPushButton("删除番剧")
        self.delete_button_anime.setObjectName("delete_button_anime")
        search_layout.addWidget(self.delete_button_anime)  # 添加到布局

        # 更改番剧按钮
        self.change_button_anime = QtWidgets.QPushButton("更改番剧")
        self.change_button_anime.setObjectName("change_button_anime")
        search_layout.addWidget(self.change_button_anime)  # 添加到布局

        main_layout.addWidget(self.search_frame_anime)  # 搜索框添加到主布局

        # 表格：番剧信息展示表格
        self.anime_table = QtWidgets.QTableWidget()
        self.anime_table.setObjectName("anime_table")
        self.anime_table.setColumnCount(5)  # 示例列数
        self.anime_table.setHorizontalHeaderLabels(["番剧ID", "名称", "类型", "出版社ID", "发行年份与季度"])
        self.anime_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.anime_table.setStyleSheet(
            f"""
            QWidget {{
                background-image: url({self.background});
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }}
            """
        )
        self.anime_table.verticalHeader().setVisible(False)  # 隐藏行号
        # 设置垂直滚动条总是显示
        self.anime_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # 设置水平滚动条根据需要显示
        self.anime_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        main_layout.addWidget(self.anime_table)  # 表格添加到主布局

    def setupPlatformTab(self, tab):
        """设置平台管理界面"""
        # 创建主布局：垂直布局
        main_layout = QtWidgets.QVBoxLayout(tab)  # 主布局管理整个 tab 页
        main_layout.setContentsMargins(10, 10, 10, 10)  # 设置四周的边距
        main_layout.setSpacing(10)  # 控件之间的间距

        # 搜索框整体框架（水平布局）
        self.search_frame_platform = QtWidgets.QFrame()
        self.search_frame_platform.setObjectName("search_frame_platform")
        search_layout = QtWidgets.QHBoxLayout(self.search_frame_platform)  # 水平布局管理搜索框
        search_layout.setContentsMargins(0, 0, 0, 0)  # 搜索框的边距
        search_layout.setSpacing(10)  # 搜索框内部控件间距

        # 搜索输入框
        self.search_edit_platform = QtWidgets.QLineEdit()
        self.search_edit_platform.setPlaceholderText("搜索平台信息（支持模糊搜索by名字）")
        self.search_edit_platform.setObjectName("search_edit_platform")
        search_layout.addWidget(self.search_edit_platform)  # 添加到布局

        # 搜索按钮
        self.search_button_platform = QtWidgets.QPushButton("搜索")
        self.search_button_platform.setObjectName("search_button_platform")
        search_layout.addWidget(self.search_button_platform)  # 添加到布局

        # 添加平台按钮
        self.add_button_platform = QtWidgets.QPushButton("添加平台")
        self.add_button_platform.setObjectName("add_button_platform")
        search_layout.addWidget(self.add_button_platform)  # 添加到布局

        # 删除平台按钮
        self.delete_button_platform = QtWidgets.QPushButton("删除平台")
        self.delete_button_platform.setObjectName("delete_button_platform")
        search_layout.addWidget(self.delete_button_platform)  # 添加到布局

        # 更改番剧按钮
        self.change_button_platform = QtWidgets.QPushButton("更改平台")
        self.change_button_platform.setObjectName("change_button_platform")
        search_layout.addWidget(self.change_button_platform)  # 添加到布局

        main_layout.addWidget(self.search_frame_platform)  # 搜索框添加到主布局

        # 表格：平台信息展示表格
        self.platform_table = QtWidgets.QTableWidget()
        self.platform_table.setObjectName("platform_table")
        self.platform_table.setColumnCount(4)  # 示例列数
        self.platform_table.setHorizontalHeaderLabels(["平台ID", "名称", "购入番剧数量", "用户数量"])
        self.platform_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.platform_table.setStyleSheet(
            f"""
            QWidget {{
                background-image: url({self.background});
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }}
            """
        )
        self.platform_table.verticalHeader().setVisible(False)  # 隐藏行号
        # 设置垂直滚动条总是显示
        self.platform_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # 设置水平滚动条根据需要显示
        self.platform_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        main_layout.addWidget(self.platform_table)  # 表格添加到主布局

    def setupUserTab(self, tab):
        """设置用户管理界面"""
        # 创建主布局：垂直布局
        main_layout = QtWidgets.QVBoxLayout(tab)
        main_layout.setContentsMargins(10, 10, 10, 10)  # 设置四周的边距
        main_layout.setSpacing(10)  # 控件之间的间距

        # 搜索框整体框架（水平布局）
        self.search_frame_user = QtWidgets.QFrame()
        self.search_frame_user.setObjectName("search_frame_user")
        search_layout = QtWidgets.QHBoxLayout(self.search_frame_user)
        search_layout.setContentsMargins(0, 0, 0, 0)  # 搜索框的边距
        search_layout.setSpacing(10)  # 搜索框内部控件间距

        # 搜索输入框
        self.search_edit_user = QtWidgets.QLineEdit()
        self.search_edit_user.setPlaceholderText("搜索用户信息（支持模糊搜索by名字）")
        self.search_edit_user.setObjectName("search_edit_user")
        search_layout.addWidget(self.search_edit_user)

        # 搜索按钮
        self.search_button_user = QtWidgets.QPushButton("搜索")
        self.search_button_user.setObjectName("search_button_user")
        search_layout.addWidget(self.search_button_user)

        # 添加用户按钮
        self.add_button_user = QtWidgets.QPushButton("添加用户")
        self.add_button_user.setObjectName("add_button_user")
        search_layout.addWidget(self.add_button_user)

        # 删除用户按钮
        self.delete_button_user = QtWidgets.QPushButton("删除用户")
        self.delete_button_user.setObjectName("delete_button_user")
        search_layout.addWidget(self.delete_button_user)

        # 更改用户按钮
        self.change_button_user = QtWidgets.QPushButton("更改用户")
        self.change_button_user.setObjectName("change_button_user")
        search_layout.addWidget(self.change_button_user)  # 添加到布局

        main_layout.addWidget(self.search_frame_user)# 搜索框添加到主布局

        # 用户信息展示表格
        self.user_table = QtWidgets.QTableWidget()
        self.user_table.setObjectName("user_table")
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(["用户ID", "用户名", "平台ID", "追番数量"])
        self.user_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.user_table.setStyleSheet(
            f"""
            QWidget {{
                background-image: url({self.background});
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }}
            """
        )
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.user_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        main_layout.addWidget(self.user_table)

    def setupPlatformPurchaseTab(self, tab):
        """设置平台购番管理界面"""
        # 创建主布局：垂直布局
        main_layout = QtWidgets.QVBoxLayout(tab)
        main_layout.setContentsMargins(10, 10, 10, 10)  # 设置四周的边距
        main_layout.setSpacing(10)  # 控件之间的间距

        # 搜索框整体框架（水平布局）
        self.search_frame_PlatformPurchase = QtWidgets.QFrame()
        self.search_frame_PlatformPurchase.setObjectName("search_frame_PlatformPurchase")
        search_layout = QtWidgets.QHBoxLayout(self.search_frame_PlatformPurchase)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(10)

        # 搜索输入框
        self.search_edit_PlatformPurchase = QtWidgets.QLineEdit()
        self.search_edit_PlatformPurchase.setPlaceholderText("搜索平台购番（支持模糊搜索by平台名字）")
        self.search_edit_PlatformPurchase.setObjectName("search_edit_PlatformPurchase")
        search_layout.addWidget(self.search_edit_PlatformPurchase)

        # 搜索按钮
        self.search_button_PlatformPurchase = QtWidgets.QPushButton("搜索")
        self.search_button_PlatformPurchase.setObjectName("search_button_PlatformPurchase")
        search_layout.addWidget(self.search_button_PlatformPurchase)

        # 添加平台番剧购入按钮
        self.add_button_PlatformPurchase = QtWidgets.QPushButton("添加平台番剧购入")
        self.add_button_PlatformPurchase.setObjectName("add_button_PlatformPurchase")
        search_layout.addWidget(self.add_button_PlatformPurchase)

        # 删除平台番剧购入按钮
        self.delete_button_PlatformPurchase = QtWidgets.QPushButton("删除平台番剧购入")
        self.delete_button_PlatformPurchase.setObjectName("delete_button_PlatformPurchase")
        search_layout.addWidget(self.delete_button_PlatformPurchase)

        main_layout.addWidget(self.search_frame_PlatformPurchase)

        # 平台购番展示表格
        self.PlatformPurchase_table = QtWidgets.QTableWidget()
        self.PlatformPurchase_table.setObjectName("PlatformPurchase_table")
        self.PlatformPurchase_table.setColumnCount(5)
        self.PlatformPurchase_table.setHorizontalHeaderLabels(["平台ID", "番剧ID", "平台名字", "番剧名字", "季度"])
        self.PlatformPurchase_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.PlatformPurchase_table.setStyleSheet(
            f"""
            QWidget {{
                background-image: url({self.background});
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }}
            """
        )
        self.PlatformPurchase_table.verticalHeader().setVisible(False)
        self.PlatformPurchase_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.PlatformPurchase_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        main_layout.addWidget(self.PlatformPurchase_table)

    def setupUserFollowingTab(self, tab):
        """设置用户订阅番剧管理界面"""
        # 创建主布局：垂直布局
        main_layout = QtWidgets.QVBoxLayout(tab)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 搜索框整体框架（水平布局）
        self.search_frame_UserFollowing = QtWidgets.QFrame()
        self.search_frame_UserFollowing.setObjectName("search_frame_UserFollowing")
        search_layout = QtWidgets.QHBoxLayout(self.search_frame_UserFollowing)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(10)

        # 搜索输入框
        self.search_edit_UserFollowing = QtWidgets.QLineEdit()
        self.search_edit_UserFollowing.setPlaceholderText("搜索番剧订阅信息（支持模糊搜索by番剧名字）")
        self.search_edit_UserFollowing.setObjectName("search_edit_UserFollowing")
        search_layout.addWidget(self.search_edit_UserFollowing)

        # 搜索按钮
        self.search_button_UserFollowing = QtWidgets.QPushButton("搜索")
        self.search_button_UserFollowing.setObjectName("search_button_UserFollowing")
        search_layout.addWidget(self.search_button_UserFollowing)

        # 添加用户番剧订阅按钮
        self.add_button_UserFollowing = QtWidgets.QPushButton("添加用户番剧订阅")
        self.add_button_UserFollowing.setObjectName("add_button_UserFollowing")
        search_layout.addWidget(self.add_button_UserFollowing)

        # 删除用户番剧订阅按钮
        self.delete_button_UserFollowing = QtWidgets.QPushButton("删除用户番剧订阅")
        self.delete_button_UserFollowing.setObjectName("delete_button_UserFollowing")
        search_layout.addWidget(self.delete_button_UserFollowing)

        # 把搜索框加入main_layout
        main_layout.addWidget(self.search_frame_UserFollowing)

        # 用户订阅番剧展示表格
        self.UserFollowing_table = QtWidgets.QTableWidget()
        self.UserFollowing_table.setObjectName("UserFollowing_table")
        self.UserFollowing_table.setColumnCount(6)
        self.UserFollowing_table.setHorizontalHeaderLabels(["平台ID", "用户ID", "番剧ID", "平台名", "用户名", "番剧名"])
        self.UserFollowing_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.UserFollowing_table.setStyleSheet(
            f"""
            QWidget {{
                background-image: url({self.background});
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }}
            """)
        self.UserFollowing_table.verticalHeader().setVisible(False)
        self.UserFollowing_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.UserFollowing_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        main_layout.addWidget(self.UserFollowing_table)

    def setupExtraTab(self, tab):
        # 背景图片路径（使用绝对路径）
        picture_path1 = os.path.abspath('./picture/picture8.jpg')  # 确保图片路径和格式正确
        picture_path2 = os.path.abspath('./picture/picture3.jpg')  # 确保图片路径和格式正确
        # 主布局
        main_layout = QtWidgets.QVBoxLayout(tab)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 添加拉伸因子，推动按钮到中心
        main_layout.addStretch(1)

        # 第一个按钮：initDataButton
        self.initDataButton = QtWidgets.QPushButton("初始化数据")
        self.initDataButton.setObjectName("initDataButton")
        self.initDataButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.initDataButton.setIcon(QtGui.QIcon(picture_path1))  # 设置按钮图标
        self.initDataButton.setIconSize(QtCore.QSize(400, 300))  # 设置图标大小
        main_layout.addWidget(self.initDataButton)

        # 第二个按钮：deleteAllButton
        self.deleteAllButton = QtWidgets.QPushButton("删除所有数据")
        self.deleteAllButton.setObjectName("deleteAllButton")
        self.deleteAllButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.deleteAllButton.setIcon(QtGui.QIcon(picture_path2))  # 设置按钮图标
        self.deleteAllButton.setIconSize(QtCore.QSize(400, 300))  # 设置图标大小
        main_layout.addWidget(self.deleteAllButton)

        # 添加拉伸因子，推动按钮到中心
        main_layout.addStretch(1)

        # 设置按钮的样式
        button_style = """
            QPushButton {
                background-color: transparent;  # 透明背景
                color: white;               # 文字颜色
                font-size: 19px;            # 字体大小
                border: 5px solid #45a049;  # 边框
                border-radius: 10px;        # 圆角
                padding: 10px;              # 内边距
            }
            QPushButton:hover {
                background-color: #45a049;  # 鼠标悬停时的背景颜色
            }
        """

        # 应用样式到按钮
        self.initDataButton.setStyleSheet(button_style)
        self.deleteAllButton.setStyleSheet(button_style)


