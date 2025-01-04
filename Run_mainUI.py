import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QLineEdit, QTableWidgetItem, QMessageBox, QDialog
from UI.main_ui import Ui_MainWindow  # 导入生成的界面类
from UI.extra_anime import AddAnimeBox, DeleteAnimeBox, ChangeAnimeBox
from UI.extra_publisher import AddPublisherBox, DeletePublisherBox, ChangePublisherBox
from UI.extra_platform import AddPlatformBox, DeletePlatformBox, ChangePlatformBox
from UI.extra_user import AddUserBox, DeleteUserBox, ChangeUserBox
from UI.extra_platformPurchase import AddPlatformPurchaseBox, DeletePlatformPurchaseBox
from UI.extra_userFollow import AddUserFollowingBox, DeleteUserFollowingBox
import sql_manager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dialog = QDialog(self)
        sql_file = "add_basedata.sql"
        # 初始化各个模块的管理类
        self.publisher_manager = PublisherManager(self.ui)
        self.anime_manager = AnimeManager(self.ui)
        self.platform_manager = PlatformManager(self.ui)
        self.user_manager = UserManager(self.ui)
        self.platform_purchase_manager = PlatformPurchaseManager(self.ui)
        self.user_following_manager = UserFollowingManager(self.ui)

        self.ui.initDataButton.clicked.connect(lambda: self.on_init_database_clicked(sql_file))
        self.ui.deleteAllButton.clicked.connect(lambda: self.on_delete_all_clicked())
    def on_init_database_clicked(self, sql_file):
        check = sql_manager.DatabaseManager.init_data(sql_file)
        if check:
            QMessageBox.information(self.dialog, "成功", "数据初始化成功！")
            self.publisher_manager.refresh_table()
            self.anime_manager.refresh_table()
            self.platform_manager.refresh_table()
            self.user_manager.refresh_table()
            self.platform_purchase_manager.refresh_table()
            self.user_following_manager.refresh_table()
            return True
        else:
            QMessageBox.warning(self.dialog, "错误", "数据初始化失败！(数据重复)")
            return False

    def on_delete_all_clicked(self):
        check = sql_manager.DatabaseManager.delete_all()
        if check:
            QMessageBox.information(self.dialog, "成功", "数据删除成功！")
            self.publisher_manager.refresh_table()
            self.anime_manager.refresh_table()
            self.platform_manager.refresh_table()
            self.user_manager.refresh_table()
            self.platform_purchase_manager.refresh_table()
            self.user_following_manager.refresh_table()
            return True
        else:
            QMessageBox.warning(self.dialog, "错误", "数据删除失败！(数据已经无了)")

class PublisherManager:
    def __init__(self, UI):
        """初始化出版社管理器"""
        self.ui = UI
        self.tab = self.ui.publisher_tab
        self.table = self.tab.findChild(QTableWidget, "publisher_table")
        self.search_edit = self.tab.findChild(QLineEdit, "search_edit_publisher")
        self.add_publisher_box = AddPublisherBox()
        self.delete_publisher_box = DeletePublisherBox()
        self.change_publisher_box = ChangePublisherBox()
        self.init_all()

    def init_all(self):
        """初始化"""
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["出版社ID", "名称", "制作番剧数量"])
        self.refresh_table()
        self.ui.search_button_publisher.clicked.connect(self.search)
        # add
        self.ui.add_button_publisher.clicked.connect(self.add_publisher_box.show)
        self.add_publisher_box.publisher_added.connect(self.refresh_table)
        # delete
        self.ui.delete_button_publisher.clicked.connect(self.delete_publisher_box.show)
        self.delete_publisher_box.publisher_deleted.connect(self.refresh_table)
        # change
        self.ui.change_button_publisher.clicked.connect(self.change_publisher_box.show)
        self.change_publisher_box.publisher_changed.connect(self.refresh_table)

    def refresh_table(self):
        """刷新表格数据"""
        # 从数据库获取所有出版社数据
        publishers = sql_manager.PublisherManager.get_all_publishers()
        # 清空表格
        self.table.setRowCount(0)
        # 填充数据
        for row, publisher in enumerate(publishers):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(publisher['PublisherID'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(publisher['Name'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(publisher['ProductionCount'])))

    def search(self):
        """搜索出版社"""
        search_text = self.search_edit.text().strip()
        if not search_text:
            self.refresh_table()
            return
        # 执行搜索
        results = sql_manager.PublisherManager.get_publishers_by_name(search_text)
        # 更新表格
        self.table.setRowCount(0)
        for row, publisher in enumerate(results):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(publisher['PublisherID'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(publisher['Name'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(publisher['ProductionCount'])))

class AnimeManager:
    def __init__(self,UI):
        """初始化番剧管理器"""
        self.ui = UI
        self.tab = self.ui.anime_tab
        self.table = self.tab.findChild(QTableWidget, "anime_table")
        self.search_edit = self.tab.findChild(QLineEdit, "search_edit_anime")
        self.add_anime_box = AddAnimeBox()
        self.delete_anime_box = DeleteAnimeBox()
        self.change_anime_box = ChangeAnimeBox()
        self.init_all()

    def init_all(self):
        """初始化"""
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["番剧ID", "名称", "类型", "出版社ID", "发行年份与季度"])
        self.refresh_table()
        self.ui.search_button_anime.clicked.connect(self.search)
        # add
        self.ui.add_button_anime.clicked.connect(self.add_anime_box.show)
        self.add_anime_box.anime_added.connect(self.refresh_table)
        # delete
        self.ui.delete_button_anime.clicked.connect(self.delete_anime_box.show)
        self.delete_anime_box.anime_deleted.connect(self.refresh_table)
        # change
        self.ui.change_button_anime.clicked.connect(self.change_anime_box.show)
        self.change_anime_box.anime_changed.connect(self.refresh_table)
    def refresh_table(self):
        """刷新表格数据"""
        # 从数据库获取所有番剧数据
        animes = sql_manager.AnimeManager.get_all_animes()  # 这个方法需要在sql_manager中实现
        # 清空表格
        self.table.setRowCount(0)
        # 填充数据
        for row, anime in enumerate(animes):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(anime['AnimeID'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(anime['Name'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(anime['Genre'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(anime['PublisherID'])))
            self.table.setItem(row, 4, QTableWidgetItem(str(anime['YearQuarter'])))

    def search(self):
        """搜索番剧"""
        search_text = self.search_edit.text().strip()
        if not search_text:
            self.refresh_table()
            return
        # 执行搜索
        results = sql_manager.AnimeManager.get_anime_by_name(search_text)  # 这个方法需要在sql_manager中实现
        # 更新表格
        self.table.setRowCount(0)
        for row, anime in enumerate(results):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(anime['AnimeID'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(anime['Name'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(anime['Genre'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(anime['PublisherID'])))
            self.table.setItem(row, 4, QTableWidgetItem(str(anime['YearQuarter'])))

class PlatformManager:
    def __init__(self, UI):
        """初始化平台管理器"""
        self.ui = UI
        self.tab = self.ui.platform_tab
        self.table = self.tab.findChild(QTableWidget, "platform_table")
        self.search_edit = self.tab.findChild(QLineEdit, "search_edit_platform")
        self.add_platform_box = AddPlatformBox()
        self.delete_platform_box = DeletePlatformBox()
        self.change_platform_box = ChangePlatformBox()
        self.init_all()

    def init_all(self):
        """初始化"""
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["平台ID", "名称", "购入番剧数量", "用户数量"])
        self.refresh_table()
        self.ui.search_button_platform.clicked.connect(self.search)
        # add
        self.ui.add_button_platform.clicked.connect(self.add_platform_box.show)
        self.add_platform_box.platform_added.connect(self.refresh_table)
        # delete
        self.ui.delete_button_platform.clicked.connect(self.delete_platform_box.show)
        self.delete_platform_box.platform_deleted.connect(self.refresh_table)
        # change
        self.ui.change_button_platform.clicked.connect(self.change_platform_box.show)
        self.change_platform_box.platform_changed.connect(self.refresh_table)

    def refresh_table(self):
        """刷新表格数据"""
        # 从数据库获取所有平台数据
        platforms = sql_manager.PlatformManager.get_all_platforms()
        # 清空表格
        self.table.setRowCount(0)
        # 填充数据
        for row, platform in enumerate(platforms):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(platform['PlatformID'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(platform['Name'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(platform['PurchasedAnimeCount'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(platform['UserCount'])))

    def search(self):
        """搜索平台"""
        search_text = self.search_edit.text().strip()
        if not search_text:
            self.refresh_table()
            return
        # 执行搜索
        results = sql_manager.PlatformManager.get_platforms_by_name(search_text)
        # 更新表格
        self.table.setRowCount(0)
        for row, platform in enumerate(results):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(platform['PlatformID'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(platform['Name'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(platform['PurchasedAnimeCount'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(platform['UserCount'])))

class UserManager:
    def __init__(self, UI):
        """初始化用户管理器"""
        self.ui = UI
        self.tab = self.ui.user_tab
        self.table = self.tab.findChild(QTableWidget, "user_table")
        self.search_edit = self.tab.findChild(QLineEdit, "search_edit_user")
        self.add_user_box = AddUserBox()
        self.delete_user_box = DeleteUserBox()
        self.change_user_box = ChangeUserBox()
        self.init_all()

    def init_all(self):
        """初始化"""
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["用户ID", "用户名", "所属平台ID", "追番数量"])
        self.refresh_table()
        self.ui.search_button_user.clicked.connect(self.search)
        # add
        self.ui.add_button_user.clicked.connect(self.add_user_box.show)
        self.add_user_box.user_added.connect(self.refresh_table)
        # delete
        self.ui.delete_button_user.clicked.connect(self.delete_user_box.show)
        self.delete_user_box.user_deleted.connect(self.refresh_table)
        # change
        self.ui.change_button_user.clicked.connect(self.change_user_box.show)
        self.change_user_box.user_changed.connect(self.refresh_table)

    def refresh_table(self):
        """刷新表格数据"""
        # 从数据库获取所有用户数据
        users = sql_manager.UserManager.get_all_users()
        # 清空表格
        self.table.setRowCount(0)
        # 填充数据
        for row, user in enumerate(users):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(user['UserID'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(user['Username'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(user['PlatformID'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(user['FollowingAnimeCount'])))

    def search(self):
        """搜索用户"""
        search_text = self.search_edit.text().strip()
        if not search_text:
            self.refresh_table()
            return
        # 执行搜索
        results = sql_manager.UserManager.get_users_by_username(search_text)
        # 更新表格
        self.table.setRowCount(0)
        for row, user in enumerate(results):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(user['UserID'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(user['Username'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(user['PlatformID'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(user['FollowingAnimeCount'])))

class PlatformPurchaseManager:
    def __init__(self, UI):
        """初始化平台购买管理器"""
        self.ui = UI
        self.tab = self.ui.PlatformPurchase_tab
        self.table = self.tab.findChild(QTableWidget, "PlatformPurchase_table")
        self.search_edit = self.tab.findChild(QLineEdit, "search_edit_PlatformPurchase")
        self.add_platform_purchase_box = AddPlatformPurchaseBox()
        self.delete_platform_purchase_box = DeletePlatformPurchaseBox()
        self.init_all()

    def init_all(self):
        """初始化"""
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["平台ID", "番剧ID", "平台名字", "番剧名字", "季度"])
        self.refresh_table()
        self.ui.search_button_PlatformPurchase.clicked.connect(self.search)
        # add
        self.ui.add_button_PlatformPurchase.clicked.connect(self.add_platform_purchase_box.show)
        self.add_platform_purchase_box.purchase_added.connect(self.refresh_table)
        # delete
        self.ui.delete_button_PlatformPurchase.clicked.connect(self.delete_platform_purchase_box.show)
        self.delete_platform_purchase_box.purchase_deleted.connect(self.refresh_table)

    def refresh_table(self):
        """刷新表格数据"""
        # 从数据库获取所有平台购买数据
        purchases = sql_manager.PlatformPurchaseManager.get_all_purchases()
        # 清空表格
        self.table.setRowCount(0)
        # 填充数据
        for row, purchase in enumerate(purchases):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(purchase['PlatformID'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(purchase['AnimeID'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(purchase['PlatformName'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(purchase['AnimeName'])))
            self.table.setItem(row, 4, QTableWidgetItem(str(purchase['YearQuarter'])))

    def search(self):
        """搜索平台购买记录"""
        search_text = self.search_edit.text().strip()
        if not search_text:
            self.refresh_table()
            return
        # 执行搜索
        results = sql_manager.PlatformPurchaseManager.get_purchases_by_platform_name(search_text)
        # 更新表格
        self.table.setRowCount(0)
        for row, purchase in enumerate(results):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(purchase['PlatformID'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(purchase['AnimeID'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(purchase['PlatformName'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(purchase['AnimeName'])))
            self.table.setItem(row, 4, QTableWidgetItem(str(purchase['YearQuarter'])))

class UserFollowingManager:
    def __init__(self, UI):
        """初始化用户关注管理器"""
        self.ui = UI
        self.tab = self.ui.UserFollowing_tab
        self.table = self.tab.findChild(QTableWidget, "UserFollowing_table")
        self.search_edit = self.tab.findChild(QLineEdit, "search_edit_UserFollowing")
        self.add_following_box = AddUserFollowingBox()
        self.delete_following_box = DeleteUserFollowingBox()
        self.init_all()

    def init_all(self):
        """初始化"""
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["平台ID", "用户ID", "番剧ID", "平台名", "用户名", "番剧名"])
        self.refresh_table()
        self.ui.search_button_UserFollowing.clicked.connect(self.search)
        # add
        self.ui.add_button_UserFollowing.clicked.connect(self.add_following_box.show)
        self.add_following_box.user_following_added.connect(self.refresh_table)
        # delete
        self.ui.delete_button_UserFollowing.clicked.connect(self.delete_following_box.show)
        self.delete_following_box.user_following_deleted.connect(self.refresh_table)

    def refresh_table(self):
        """刷新表格数据"""
        # 从数据库获取所有用户关注数据
        followings = sql_manager.UserFollowingManager.get_all_followings()
        # 清空表格
        self.table.setRowCount(0)
        # 填充数据
        for row, following in enumerate(followings):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(following['PlatformID'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(following['UserID'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(following['AnimeID'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(following['PlatformName'])))
            self.table.setItem(row, 4, QTableWidgetItem(str(following['UserName'])))
            self.table.setItem(row, 5, QTableWidgetItem(str(following['AnimeName'])))

    def search(self):
        """搜索用户关注"""
        search_text = self.search_edit.text().strip()
        if not search_text:
            self.refresh_table()
            return
        # 执行搜索
        results = sql_manager.UserFollowingManager.get_followings_by_anime_name(search_text)
        # 更新表格
        self.table.setRowCount(0)
        for row, following in enumerate(results):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(following['PlatformID'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(following['UserID'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(following['AnimeID'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(following['PlatformName'])))
            self.table.setItem(row, 4, QTableWidgetItem(str(following['UserName'])))
            self.table.setItem(row, 5, QTableWidgetItem(str(following['AnimeName'])))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

