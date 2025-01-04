from sql_manager import UserFollowingManager
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox

class Ui_UserFollowingBox(object):
    def setupUi(self, UserFollowingBox):
        UserFollowingBox.setObjectName("UserFollowingBox")
        UserFollowingBox.setWindowIcon(QtGui.QIcon("./picture/icon_2.png"))
        UserFollowingBox.resize(550, 300)

        # 主布局
        self.main_layout = QtWidgets.QVBoxLayout(UserFollowingBox)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # 提示信息
        self.msg = QtWidgets.QLabel(UserFollowingBox)
        self.msg.setObjectName("msg")
        self.main_layout.addWidget(self.msg, alignment=QtCore.Qt.AlignCenter)

        # 用户ID
        self.user_id_layout = QtWidgets.QHBoxLayout()
        self.label_user_id = QtWidgets.QLabel(UserFollowingBox)
        self.label_user_id.setObjectName("label_user_id")
        self.user_id_layout.addWidget(self.label_user_id)
        self.user_id_edit = QtWidgets.QLineEdit(UserFollowingBox)
        self.user_id_edit.setClearButtonEnabled(True)
        self.user_id_edit.setObjectName("user_id_edit")
        self.user_id_layout.addWidget(self.user_id_edit)
        self.main_layout.addLayout(self.user_id_layout)

        # 番剧ID
        self.anime_id_layout = QtWidgets.QHBoxLayout()
        self.label_anime_id = QtWidgets.QLabel(UserFollowingBox)
        self.label_anime_id.setObjectName("label_anime_id")
        self.anime_id_layout.addWidget(self.label_anime_id)
        self.anime_id_edit = QtWidgets.QLineEdit(UserFollowingBox)
        self.anime_id_edit.setClearButtonEnabled(True)
        self.anime_id_edit.setObjectName("anime_id_edit")
        self.anime_id_layout.addWidget(self.anime_id_edit)
        self.main_layout.addLayout(self.anime_id_layout)

        # 平台ID（AnimePlatformID）
        self.platform_id_layout = QtWidgets.QHBoxLayout()
        self.label_platform_id = QtWidgets.QLabel(UserFollowingBox)
        self.label_platform_id.setObjectName("label_platform_id")
        self.platform_id_layout.addWidget(self.label_platform_id)
        self.platform_id_edit = QtWidgets.QLineEdit(UserFollowingBox)
        self.platform_id_edit.setClearButtonEnabled(True)
        self.platform_id_edit.setObjectName("platform_id_edit")
        self.platform_id_layout.addWidget(self.platform_id_edit)
        self.main_layout.addLayout(self.platform_id_layout)

        # 按钮布局
        self.button_layout = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton(UserFollowingBox)
        self.ok_button.setObjectName("ok_button")
        self.button_layout.addWidget(self.ok_button, alignment=QtCore.Qt.AlignCenter)
        self.cancel_button = QtWidgets.QPushButton(UserFollowingBox)
        self.cancel_button.setObjectName("cancel_button")
        self.button_layout.addWidget(self.cancel_button, alignment=QtCore.Qt.AlignCenter)
        self.main_layout.addLayout(self.button_layout)

        self.retranslateUi(UserFollowingBox)
        QtCore.QMetaObject.connectSlotsByName(UserFollowingBox)

    def retranslateUi(self, UserFollowingBox):
        _translate = QtCore.QCoreApplication.translate
        UserFollowingBox.setWindowTitle(_translate("UserFollowingBox", "添加or删除用户追番记录"))
        self.msg.setText(_translate("UserFollowingBox", "请输入用户追番的记录："))
        self.label_user_id.setText(_translate("UserFollowingBox", "用户ID"))
        self.label_anime_id.setText(_translate("UserFollowingBox", "番剧ID"))
        self.label_platform_id.setText(_translate("UserFollowingBox", "平台ID"))
        self.ok_button.setText(_translate("UserFollowingBox", "确定"))
        self.cancel_button.setText(_translate("UserFollowingBox", "取消"))

class UserFollowing:
    """用户追番实体类"""
    def __init__(self):
        self.platform_id = ""
        self.user_id = ""
        self.anime_id = ""

    def checkInfo(self):
        """检查追番记录信息是否完整"""
        if not self.user_id:
            return False, "用户ID不能为空"
        if not self.anime_id:
            return False, "番剧ID不能为空"
        if not self.platform_id:
            return False, "平台ID不能为空"
        return True, "数据完整"

class UserFollowingBox(QWidget):
    """用户追番记录编辑盒 - 基类"""
    def __init__(self):
        super().__init__()
        self.dialog = QDialog()
        window = Ui_UserFollowingBox()
        window.setupUi(self.dialog)
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        # 获取 UI 元素
        self.user_id_edit = window.user_id_edit  # 用户ID
        self.anime_id_edit = window.anime_id_edit  # 番剧ID
        self.platform_id_edit = window.platform_id_edit  # 平台ID
        self.msg_label = window.msg  # 提示信息

        # 按钮
        self.ok_button = window.ok_button
        self.cancel_button = window.cancel_button
        self.ok_button.clicked.connect(self.onOkButtonClicked)
        self.cancel_button.clicked.connect(self.dialog.close)

        # 实体类
        self.user_following = UserFollowing()  # 创建 UserFollowing 实例

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

    def applyToUserFollowing(self, user_following):
        """将输入框的值应用到 UserFollowing 对象中"""
        user_following.user_id = self.user_id_edit.text().strip()
        user_following.anime_id = self.anime_id_edit.text().strip()
        user_following.platform_id = self.platform_id_edit.text().strip()

    def onFinished(self):
        """子类实现此方法以定义完成逻辑"""
        return False

class AddUserFollowingBox(UserFollowingBox):  # 继承自 UserFollowingBox
    user_following_added = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setTitle("新增用户追番记录")
        self.setMsg("请输入用户追番的记录：")
        self.setButton("新增", "取消")

    def onFinished(self):
        """新增用户追番记录的逻辑"""
        self.applyToUserFollowing(self.user_following)
        check, info = self.user_following.checkInfo()
        if check:
            sql_check = UserFollowingManager.add_following(
                anime_platform_id=self.user_following.platform_id,
                anime_id=self.user_following.anime_id,
                user_id=self.user_following.user_id
            )
            if sql_check:
                QMessageBox.information(self.dialog, "成功", "用户追番记录新增成功！")
                self.user_following_added.emit()
                return True
            else:
                QMessageBox.warning(self.dialog, "失败", "新增失败！（可能是记录已存在或ID无效）")
                return False
        else:
            QMessageBox.warning(self.dialog, "必要信息不完整", info)
            return False

class DeleteUserFollowingBox(UserFollowingBox):  # 继承自 UserFollowingBox
    user_following_deleted = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.user_following = UserFollowing()  # 创建 UserFollowing 实例
        self.setTitle("删除用户追番记录")
        self.setMsg("请输入要删除的用户追番记录（用户ID和番剧ID）：")
        self.setButton("删除", "取消")
        self.platform_id_edit.setEnabled(False)

    def onFinished(self):
        """删除用户追番记录的逻辑"""
        user_id = self.user_id_edit.text().strip()
        anime_id = self.anime_id_edit.text().strip()
        if not user_id or not anime_id:
            QMessageBox.warning(self, "必要信息不完整", "用户ID和番剧ID不能为空！")
            return False
        else:
            if not UserFollowingManager.find_following(user_id, anime_id):
                QMessageBox.warning(self.dialog, "失败", "删除失败！（记录不存在）")
                return False
            sql_check = UserFollowingManager.delete_following(user_id,anime_id)
        if sql_check:
            QMessageBox.information(self, "成功", "追番记录删除成功！")
            self.user_following_deleted.emit()
            return True
        else:
            QMessageBox.information(self, "失败", "追番记录删除失败！（数据库删除失败，是不是ID输错了）")
            return False
