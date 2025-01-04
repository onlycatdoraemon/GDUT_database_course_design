# -*- coding: utf-8 -*-
from sql_manager import AnimeManager
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox

class Ui_AnimeBox(object):
    def setupUi(self, AnimeBox):
        AnimeBox.setObjectName("AnimeBox")
        AnimeBox.setWindowIcon(QtGui.QIcon("./picture/icon_1.png"))
        AnimeBox.resize(500, 300)

        # 使用相对布局
        self.central_layout = QtWidgets.QVBoxLayout(AnimeBox)
        self.central_layout.setContentsMargins(20, 20, 20, 20)
        self.central_layout.setSpacing(15)

        # 提示信息
        self.msg = QtWidgets.QLabel(AnimeBox)
        self.msg.setObjectName("msg")
        self.central_layout.addWidget(self.msg, alignment=QtCore.Qt.AlignCenter)

        # Form Layout for input fields
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setSpacing(10)

        # 番剧ID
        self.label_id = QtWidgets.QLabel(AnimeBox)
        self.label_id.setObjectName("label_id")
        self.id_edit = QtWidgets.QLineEdit(AnimeBox)
        self.id_edit.setClearButtonEnabled(True)
        self.id_edit.setObjectName("id_edit")
        self.form_layout.addRow(self.label_id, self.id_edit)

        # 番剧名称
        self.label_name = QtWidgets.QLabel(AnimeBox)
        self.label_name.setObjectName("label_name")
        self.name_edit = QtWidgets.QLineEdit(AnimeBox)
        self.name_edit.setClearButtonEnabled(True)
        self.name_edit.setObjectName("name_edit")
        self.form_layout.addRow(self.label_name, self.name_edit)

        # 番剧类型
        self.label_genre = QtWidgets.QLabel(AnimeBox)
        self.label_genre.setObjectName("label_genre")
        self.genre_edit = QtWidgets.QLineEdit(AnimeBox)
        self.genre_edit.setClearButtonEnabled(True)
        self.genre_edit.setObjectName("genre_edit")
        self.form_layout.addRow(self.label_genre, self.genre_edit)

        # 出版社ID
        self.label_publisher = QtWidgets.QLabel(AnimeBox)
        self.label_publisher.setObjectName("label_publisher")
        self.publisher_edit = QtWidgets.QLineEdit(AnimeBox)
        self.publisher_edit.setClearButtonEnabled(True)
        self.publisher_edit.setObjectName("publisher_edit")
        self.form_layout.addRow(self.label_publisher, self.publisher_edit)

        # 发行年份与季度
        self.label_year = QtWidgets.QLabel(AnimeBox)
        self.label_year.setObjectName("label_year")
        self.year_edit = QtWidgets.QLineEdit(AnimeBox)
        self.year_edit.setClearButtonEnabled(True)
        self.year_edit.setObjectName("year_edit")
        self.form_layout.addRow(self.label_year, self.year_edit)

        # Add form layout to central layout
        self.central_layout.addLayout(self.form_layout)

        # Buttons Layout
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setSpacing(20)

        self.ok_button = QtWidgets.QPushButton(AnimeBox)
        self.ok_button.setObjectName("ok_button")
        self.button_layout.addWidget(self.ok_button)

        self.cancel_button = QtWidgets.QPushButton(AnimeBox)
        self.cancel_button.setObjectName("cancel_button")
        self.button_layout.addWidget(self.cancel_button)

        # Add buttons layout to central layout
        self.central_layout.addLayout(self.button_layout)

        self.retranslateUi(AnimeBox)
        QtCore.QMetaObject.connectSlotsByName(AnimeBox)

    def retranslateUi(self, AnimeBox):
        _translate = QtCore.QCoreApplication.translate
        AnimeBox.setWindowTitle(_translate("AnimeBox", "添加or删除番剧信息"))
        self.msg.setText(_translate("AnimeBox", "请输入番剧的信息："))
        self.label_id.setText(_translate("AnimeBox", "番剧ID"))
        self.label_name.setText(_translate("AnimeBox", "名称"))
        self.label_genre.setText(_translate("AnimeBox", "类型"))
        self.label_publisher.setText(_translate("AnimeBox", "出版社ID"))
        self.label_year.setText(_translate("AnimeBox", "年份季度"))
        self.ok_button.setText(_translate("AnimeBox", "确定"))
        self.cancel_button.setText(_translate("AnimeBox", "取消"))

class Anime:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.genre = ""
        self.publisher_id = ""
        self.year_quarter = ""

    def checkInfo(self):
        """检查番剧信息是否完整"""
        if not self.id:
            return False, "番剧ID不能为空"
        if not self.name:
            return False, "名称不能为空"
        if not self.publisher_id:
            return False, "出版社ID不能为空"
        return True, "数据完整"

class AnimeBox(QWidget):
    """番剧信息编辑盒 - 基类"""
    def __init__(self):
        super().__init__()
        self.dialog = QDialog()
        window = Ui_AnimeBox()
        window.setupUi(self.dialog)
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        # 获取 UI 元素
        self.id_edit = window.id_edit  # 番剧ID
        self.name_edit = window.name_edit  # 番剧名称
        self.genre_edit = window.genre_edit  # 番剧类型
        self.publisher_edit = window.publisher_edit  # 出版社ID
        self.year_edit = window.year_edit  # 发行年份与季度
        self.msg_label = window.msg  # 提示信息

        # 按钮
        self.ok_button = window.ok_button
        self.cancel_button = window.cancel_button
        self.ok_button.clicked.connect(self.onOkButtonClicked)
        self.cancel_button.clicked.connect(self.dialog.close)

    def onOkButtonClicked(self):
        """确定按钮点击事件"""
        if self.onFinished():
            self.dialog.close()

    def show(self):
        """显示对话框"""
        self.dialog.show()

    def setTitle(self, title):
        """设置窗口标题"""
        self.dialog.setWindowTitle(title)

    def setMsg(self, text):
        """设置提示信息"""
        self.msg_label.setText(text)

    def setButton(self, ok, cancel=None):
        """设置按钮文本"""
        self.ok_button.setText(ok)
        if cancel is not None:
            self.cancel_button.setText(cancel)

    def applyToAnime(self, anime):
        """将输入框的值应用到番剧对象中"""
        anime.id = self.id_edit.text().strip()
        anime.name = self.name_edit.text().strip()
        anime.genre = self.genre_edit.text().strip()
        anime.publisher_id = self.publisher_edit.text().strip()
        anime.year_quarter = self.year_edit.text().strip()

    def onFinished(self):
        """子类实现此方法以定义完成逻辑"""
        return False

class AddAnimeBox(AnimeBox):  # 继承自 AnimeBox
    anime_added = pyqtSignal()
    def __init__(self):
        super().__init__()  # 调用 AnimeBox 的构造函数
        self.anime = Anime()  # 创建 Anime 实例
        # 设置窗口标题和按钮文本
        self.setTitle("新增番剧信息")
        self.setMsg("请输入要加入的番剧信息\n（注意填写出版社ID要在数据库中哦！！！）")
        self.setButton("新增", "取消")
    def onFinished(self):
        """新增番剧的逻辑"""
        self.applyToAnime(self.anime)
        check, info = self.anime.checkInfo()  # 检查信息完整性
        if check:
            sql_check = AnimeManager.add_anime(
                anime_id=self.anime.id,
                name=self.anime.name,
                genre=self.anime.genre,
                publisher_id=self.anime.publisher_id,
                year_quarter=self.anime.year_quarter
            )
            if sql_check:
                QMessageBox.information(self.dialog, "成功", "番剧信息新增成功！")
                self.anime_added.emit()  # 发射信号
                return True
            else:
                QMessageBox.warning(self.dialog, "失败", "番剧信息新增失败（你输入的出版社ID不存在或者番剧ID重复了）！")
                return False
        else:
            QMessageBox.warning(self.dialog, "你输入的信息不完整", info)
            return False

# 删除番剧信息
class DeleteAnimeBox(AnimeBox):
    anime_deleted = pyqtSignal()
    """删除番剧信息 - 继承 AnimeBox"""
    def __init__(self):
        super().__init__()  # 调用 AnimeBox 的构造函数
        self.anime = Anime()  # 创建 Anime 实例

        self.setTitle("删除番剧信息")
        self.setMsg("请输入要删除的番剧或名字")
        self.setButton("删除", "取消")

        # 仅保留番剧ID和名字输入框
        self.genre_edit.setEnabled(False)
        self.publisher_edit.setEnabled(False)
        self.year_edit.setEnabled(False)

    def onFinished(self):
        """删除逻辑"""
        anime_id = self.id_edit.text().strip()
        anime_name = self.name_edit.text().strip()
        if not anime_id and not anime_name:
            QMessageBox.warning(self.dialog, "失败", "大佬啊，番剧ID或番剧名字至少输一个！")
            return False

        if anime_id:
            if not AnimeManager.get_anime_by_id(anime_id):
                QMessageBox.warning(self.dialog, "失败", "你输入的番剧ID不存在哦！")
                return False
            sql_check = AnimeManager.delete_anime_id(anime_id)
        else:
            if not AnimeManager.get_anime_by_name(anime_name):
                QMessageBox.warning(self.dialog, "失败", "你输入的番剧名字不存在哦！")
                return False
            sql_check = AnimeManager.delete_anime_name(anime_name)
        if sql_check:
            QMessageBox.information(self.dialog, "成功", "番剧信息删除成功！")
            self.anime_deleted.emit()
            return True
        else:
            QMessageBox.warning(self.dialog, "失败", "删除数据失败！（数据库异常）")
            return False

class ChangeAnimeBox(AnimeBox):  # 继承自 AnimeBox
    anime_changed = pyqtSignal()
    def __init__(self):
        super().__init__()  # 调用 AnimeBox 的构造函数
        self.anime = Anime()  # 创建 Anime 实例
        # 设置窗口标题和按钮文本
        self.setTitle("修改番剧信息")
        self.setMsg("请输入要修改的番剧信息（番剧ID必填）")
        self.setButton("修改", "取消")
    def onFinished(self):
        """新增番剧的逻辑"""
        anime_id = self.id_edit.text().strip()
        anime_name = self.name_edit.text().strip()
        anime_genre = self.genre_edit.text().strip()
        anime_publisher_id = self.publisher_edit.text().strip()
        anime_year_quarter = self.year_edit.text().strip()
        if anime_id:
            if not AnimeManager.get_anime_by_id(anime_id):
                QMessageBox.warning(self.dialog, "失败", "你输入的番剧ID不存在哦！")
                return False
            sql_check = AnimeManager.update_anime(
                anime_id=anime_id,
                name=anime_name,
                genre=anime_genre,
                publisher_id=anime_publisher_id,
                year_quarter=anime_year_quarter
            )
            if sql_check:
                QMessageBox.information(self.dialog, "成功", "番剧信息修改成功！")
                self.anime_changed.emit()  # 发射信号
                return True
            else:
                QMessageBox.warning(self.dialog, "失败", "番剧信息修改失败！（数据库修改失败）")
                return False
        else:
            QMessageBox.warning(self.dialog, "失败", "改番好歹输个ID吧不然咋改啊")
            return False



