from sql_manager import UserManager
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox
class Ui_UserBox(object):
    def setupUi(self, UserBox):
        UserBox.setObjectName("UserBox")
        UserBox.setWindowIcon(QtGui.QIcon("./picture/icon_1.png"))
        UserBox.resize(500, 250)

        # 主布局
        self.main_layout = QtWidgets.QVBoxLayout(UserBox)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # 提示信息
        self.msg = QtWidgets.QLabel(UserBox)
        self.msg.setObjectName("msg")
        self.main_layout.addWidget(self.msg, alignment=QtCore.Qt.AlignCenter)

        # 用户ID
        self.id_layout = QtWidgets.QHBoxLayout()
        self.label_user_id = QtWidgets.QLabel(UserBox)
        self.label_user_id.setObjectName("label_user_id")
        self.id_layout.addWidget(self.label_user_id)
        self.user_id_edit = QtWidgets.QLineEdit(UserBox)
        self.user_id_edit.setClearButtonEnabled(True)
        self.user_id_edit.setObjectName("user_id_edit")
        self.id_layout.addWidget(self.user_id_edit)
        self.main_layout.addLayout(self.id_layout)

        # 用户名
        self.username_layout = QtWidgets.QHBoxLayout()
        self.label_username = QtWidgets.QLabel(UserBox)
        self.label_username.setObjectName("label_username")
        self.username_layout.addWidget(self.label_username)
        self.username_edit = QtWidgets.QLineEdit(UserBox)
        self.username_edit.setClearButtonEnabled(True)
        self.username_edit.setObjectName("username_edit")
        self.username_layout.addWidget(self.username_edit)
        self.main_layout.addLayout(self.username_layout)

        # 用户所在平台ID
        self.platform_layout = QtWidgets.QHBoxLayout()
        self.label_platform_id = QtWidgets.QLabel(UserBox)
        self.label_platform_id.setObjectName("label_platform_id")
        self.platform_layout.addWidget(self.label_platform_id)
        self.platform_id_edit = QtWidgets.QLineEdit(UserBox)
        self.platform_id_edit.setClearButtonEnabled(True)
        self.platform_id_edit.setObjectName("platform_id_edit")
        self.platform_layout.addWidget(self.platform_id_edit)
        self.main_layout.addLayout(self.platform_layout)

        # 按钮布局
        self.button_layout = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton(UserBox)
        self.ok_button.setObjectName("ok_button")
        self.button_layout.addWidget(self.ok_button, alignment=QtCore.Qt.AlignCenter)
        self.cancel_button = QtWidgets.QPushButton(UserBox)
        self.cancel_button.setObjectName("cancel_button")
        self.button_layout.addWidget(self.cancel_button, alignment=QtCore.Qt.AlignCenter)
        self.main_layout.addLayout(self.button_layout)

        self.retranslateUi(UserBox)
        QtCore.QMetaObject.connectSlotsByName(UserBox)

    def retranslateUi(self, UserBox):
        _translate = QtCore.QCoreApplication.translate
        UserBox.setWindowTitle(_translate("UserBox", "添加or删除用户信息"))
        self.msg.setText(_translate("UserBox", "请输入用户的信息："))
        self.label_user_id.setText(_translate("UserBox", "用户ID"))
        self.label_username.setText(_translate("UserBox", "用户名"))
        self.label_platform_id.setText(_translate("UserBox", "平台ID"))
        self.ok_button.setText(_translate("UserBox", "确定"))
        self.cancel_button.setText(_translate("UserBox", "取消"))

class User:
    def __init__(self):
        self.user_id = ""
        self.username = ""
        self.platform_id = ""

    def checkInfo(self):
        """检查用户信息是否完整"""
        if not self.user_id:
            return False, "用户ID不能为空"
        if not self.username:
            return False, "用户名不能为空"
        if not self.platform_id:
            return False, "平台ID不能为空"
        return True, "数据完整"

class UserBox(QWidget):
    """用户信息编辑盒 - 基类"""
    def __init__(self):
        super().__init__()
        self.dialog = QDialog()
        window = Ui_UserBox()
        window.setupUi(self.dialog)
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        # 获取 UI 元素
        self.user_id_edit = window.user_id_edit  # 用户ID
        self.username_edit = window.username_edit  # 用户名
        self.platform_id_edit = window.platform_id_edit  # 平台ID
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

    def applyToUser(self, user):
        """将输入框的值应用到用户对象中"""
        user.user_id = self.user_id_edit.text().strip()
        user.username = self.username_edit.text().strip()
        user.platform_id = self.platform_id_edit.text().strip()

    def onFinished(self):
        """子类实现此方法以定义完成逻辑"""
        return False

class AddUserBox(UserBox):
    user_added = pyqtSignal()
    """新增用户信息 - 继承 UserBox"""
    def __init__(self):
        super().__init__()
        self.user = User()
        self.setTitle("新增用户信息")
        self.setMsg("请输入用户的信息：")
        self.setButton("新增", "取消")

    def onFinished(self):
        """新增用户的逻辑"""
        self.applyToUser(self.user)
        check, info = self.user.checkInfo()
        if check:
            sql_check = UserManager.add_user(
                user_id=self.user.user_id,
                username=self.user.username,
                platform_id=self.user.platform_id
            )
            if sql_check:
                QMessageBox.information(self.dialog, "成功", "用户信息新增成功！")
                self.user_added.emit()
                return True
            else:
                QMessageBox.warning(self.dialog, "失败", "用户信息新增失败（你输入的用户ID或平台ID可能重复或不存在）！")
                return False
        else:
            QMessageBox.warning(self.dialog, "信息不完整", info)
            return False

class DeleteUserBox(UserBox):
    user_deleted = pyqtSignal()
    """删除用户信息 - 继承 UserBox"""
    def __init__(self):
        super().__init__()
        self.user = User()
        self.setTitle("删除用户信息")
        self.setMsg("请输入要删除的用户ID或用户名")
        self.setButton("删除", "取消")

        # 仅保留用户ID和用户名输入框
        self.platform_id_edit.setEnabled(False)

    def onFinished(self):
        """删除用户的逻辑"""
        user_id = self.user_id_edit.text().strip()
        username = self.username_edit.text().strip()
        if not user_id and not username:
            self.setMsg("大佬啊，用户ID或用户名至少输一个")
            return False
        if user_id:
            if not UserManager.get_user_by_id(user_id):
                QMessageBox.warning(self.dialog, "用户不存在", "用户不存在，请检查用户ID是否正确！")
                return False
            sql_check = UserManager.delete_user_by_id(user_id)
        else:
            if not UserManager.get_user_by_username(username):
                QMessageBox.warning(self.dialog, "用户不存在", "用户不存在，请检查用户名是否正确！")
                return False
            sql_check = UserManager.delete_user_by_name(username)
        if sql_check:
            QMessageBox.information(self.dialog, "成功", "用户信息删除成功！")
            self.user_deleted.emit()
            return True
        else:
            QMessageBox.warning(self.dialog, "失败", "删除用户失败！（数据库删除失败，是不是关键词输错了）")
            return False

class ChangeUserBox(UserBox):
    user_changed = pyqtSignal()
    """修改用户信息 - 继承 UserBox"""
    def __init__(self):
        super().__init__()
        self.user = User()
        self.setTitle("修改用户信息")
        self.setMsg("请输入要修改的用户信息（至少ID）：")
        self.setButton("修改", "取消")

    def onFinished(self):
        """修改用户的逻辑"""
        user_id = self.user_id_edit.text().strip()
        username = self.username_edit.text().strip()
        platform_id = self.platform_id_edit.text().strip()

        if not user_id:
            QMessageBox.warning(self.dialog, "失败", "改用户好歹输个ID吧，不然咋改啊")
            return False
        if not UserManager.get_user_by_id(user_id):
            QMessageBox.warning(self.dialog, "用户不存在", "用户不存在，请检查用户ID是否正确！")
            return False
        sql_check = UserManager.update_user(
            user_id=user_id,
            username=username,
            platform_id=platform_id
        )
        if sql_check:
            QMessageBox.information(self.dialog, "成功", "用户信息修改成功！")
            self.user_changed.emit()  # 发射信号
            return True
        else:
            QMessageBox.warning(self.dialog, "失败", "用户信息修改失败（数据库修改失败，你输入的用户ID可能不存在或平台ID无效）！")
            return False
