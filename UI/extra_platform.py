from sql_manager import PlatformManager
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox

class Ui_PlatformBox(object):
    def setupUi(self, PlatformBox):
        PlatformBox.setObjectName("PlatformBox")
        PlatformBox.setWindowIcon(QtGui.QIcon("./picture/icon_2.png"))
        PlatformBox.resize(500, 300)

        # 主布局
        self.main_layout = QtWidgets.QVBoxLayout(PlatformBox)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # 提示信息
        self.msg = QtWidgets.QLabel(PlatformBox)
        self.msg.setObjectName("msg")
        self.main_layout.addWidget(self.msg, alignment=QtCore.Qt.AlignCenter)

        # 平台ID
        self.id_layout = QtWidgets.QHBoxLayout()
        self.label_id = QtWidgets.QLabel(PlatformBox)
        self.label_id.setObjectName("label_id")
        self.id_layout.addWidget(self.label_id)
        self.id_edit = QtWidgets.QLineEdit(PlatformBox)
        self.id_edit.setClearButtonEnabled(True)
        self.id_edit.setObjectName("id_edit")
        self.id_layout.addWidget(self.id_edit)
        self.main_layout.addLayout(self.id_layout)

        # 平台名称
        self.name_layout = QtWidgets.QHBoxLayout()
        self.label_name = QtWidgets.QLabel(PlatformBox)
        self.label_name.setObjectName("label_name")
        self.name_layout.addWidget(self.label_name)
        self.name_edit = QtWidgets.QLineEdit(PlatformBox)
        self.name_edit.setClearButtonEnabled(True)
        self.name_edit.setObjectName("name_edit")
        self.name_layout.addWidget(self.name_edit)
        self.main_layout.addLayout(self.name_layout)

        # 按钮布局
        self.button_layout = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton(PlatformBox)
        self.ok_button.setObjectName("ok_button")
        self.button_layout.addWidget(self.ok_button, alignment=QtCore.Qt.AlignCenter)
        self.cancel_button = QtWidgets.QPushButton(PlatformBox)
        self.cancel_button.setObjectName("cancel_button")
        self.button_layout.addWidget(self.cancel_button, alignment=QtCore.Qt.AlignCenter)
        self.main_layout.addLayout(self.button_layout)

        self.retranslateUi(PlatformBox)
        QtCore.QMetaObject.connectSlotsByName(PlatformBox)

    def retranslateUi(self, PlatformBox):
        _translate = QtCore.QCoreApplication.translate
        PlatformBox.setWindowTitle(_translate("PlatformBox", "添加or删除平台信息"))
        self.msg.setText(_translate("PlatformBox", "请输入平台的信息："))
        self.label_id.setText(_translate("PlatformBox", "   平台ID   "))
        self.label_name.setText(_translate("PlatformBox", "    名称    "))
        self.ok_button.setText(_translate("PlatformBox", "确定"))
        self.cancel_button.setText(_translate("PlatformBox", "取消"))

class Platform:
    def __init__(self):
        self.id = ""
        self.name = ""

    def checkInfo(self):
        """检查平台信息是否完整"""
        if not self.id:
            return False, "平台ID不能为空"
        if not self.name:
            return False, "平台名称不能为空"
        return True, "数据完整"


class PlatformBox(QWidget):
    """平台信息编辑盒 - 基类"""
    def __init__(self):
        super().__init__()
        self.dialog = QDialog()
        window = Ui_PlatformBox()
        window.setupUi(self.dialog)
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        # 获取 UI 元素
        self.id_edit = window.id_edit  # 平台ID
        self.name_edit = window.name_edit  # 平台名称
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

    def applyToPlatform(self, platform):
        """将输入框的值应用到平台对象中"""
        platform.id = self.id_edit.text().strip()
        platform.name = self.name_edit.text().strip()

    def onFinished(self):
        """子类实现此方法以定义完成逻辑"""
        return False

class AddPlatformBox(PlatformBox):  # 继承自 PlatformBox
    platform_added = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.platform = Platform()  # 创建 Platform 实例
        self.setTitle("新增平台信息")
        self.setMsg("请输入要添加的平台信息")
        self.setButton("新增", "取消")

    def onFinished(self):
        """新增平台的逻辑"""
        self.applyToPlatform(self.platform)
        check, info = self.platform.checkInfo()
        if check:
            sql_check = PlatformManager.add_platform(
                platform_id=self.platform.id,
                name=self.platform.name,
            )
            if sql_check:
                QMessageBox.information(self.dialog, "成功", "平台信息新增成功！")
                self.platform_added.emit()
                return True
            else:
                QMessageBox.warning(self.dialog, "失败", "平台信息新增失败（数据库添加失败，可能平台ID重复）！")
                return False
        else:
            QMessageBox.warning(self.dialog, "你输入的平台信息不完整", info)
            return False

class DeletePlatformBox(PlatformBox):  # 继承自 PlatformBox
    platform_deleted = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.platform = Platform()  # 创建 Platform 实例
        self.setTitle("删除平台信息")
        self.setMsg("请输入要删除的平台ID或名称")
        self.setButton("删除", "取消")

    def onFinished(self):
        """删除逻辑"""
        platform_id = self.id_edit.text().strip()
        platform_name = self.name_edit.text().strip()
        if not platform_id and not platform_name:
            QMessageBox.warning(self.dialog, "失败", "至少平台名或者平台ID输入一个吧！")
            return False
        if platform_id:
            if not PlatformManager.get_platform_by_id(platform_id):
                QMessageBox.warning(self.dialog, "失败", "平台ID不存在！")
                return False
            sql_check = PlatformManager.delete_platform_by_id(platform_id)
        else:
            if not PlatformManager.get_platforms_by_name(platform_name):
                QMessageBox.warning(self.dialog, "失败", "平台名称不存在！")
                return False
            sql_check = PlatformManager.delete_platform_by_name(platform_name)
        if sql_check:
            QMessageBox.information(self.dialog, "成功", "平台信息删除成功！")
            self.platform_deleted.emit()
            return True
        else:
            QMessageBox.warning(self, "失败", "删除数据失败！（是不是关键词输错了）")
            return False


class ChangePlatformBox(PlatformBox):  # 继承自 PlatformBox
    platform_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.platform = Platform()  # 创建 Platform 实例
        self.setTitle("修改平台信息")
        self.setMsg("请输入修改的平台信息（至少输入ID）")
        self.setButton("修改", "取消")

    def onFinished(self):
        """修改平台的逻辑"""
        self.applyToPlatform(self.platform)
        if self.platform.id:
            if not PlatformManager.get_platform_by_id(self.platform.id):
                QMessageBox.warning(self.dialog, "失败", "你输入的平台ID不存在！")
                return False
            sql_check = PlatformManager.update_platform(
                platform_id=self.platform.id,
                name=self.platform.name,
            )
            if sql_check:
                QMessageBox.information(self.dialog, "成功", "平台信息修改成功！")
                self.platform_changed.emit()
                return True
            else:
                QMessageBox.warning(self.dialog, "失败", "平台信息修改失败（数据库修改失败）！")
                return False
        else:
            QMessageBox.warning(self.dialog, "失败", "改平台好歹输个ID吧不然咋改啊")
            return False
