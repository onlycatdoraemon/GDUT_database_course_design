from sql_manager import PlatformPurchaseManager
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox
class Ui_PlatformPurchaseBox(object):
    def setupUi(self, PlatformPurchaseBox):
        PlatformPurchaseBox.setObjectName("PlatformPurchaseBox")
        PlatformPurchaseBox.setWindowIcon(QtGui.QIcon("./picture/icon_3.png"))
        PlatformPurchaseBox.resize(500, 200)

        # 主布局
        self.main_layout = QtWidgets.QVBoxLayout(PlatformPurchaseBox)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # 提示信息
        self.msg = QtWidgets.QLabel(PlatformPurchaseBox)
        self.msg.setObjectName("msg")
        self.main_layout.addWidget(self.msg, alignment=QtCore.Qt.AlignCenter)

        # 平台ID
        self.id_layout = QtWidgets.QHBoxLayout()
        self.label_platform_id = QtWidgets.QLabel(PlatformPurchaseBox)
        self.label_platform_id.setObjectName("label_platform_id")
        self.id_layout.addWidget(self.label_platform_id)
        self.platform_id_edit = QtWidgets.QLineEdit(PlatformPurchaseBox)
        self.platform_id_edit.setClearButtonEnabled(True)
        self.platform_id_edit.setObjectName("platform_id_edit")
        self.id_layout.addWidget(self.platform_id_edit)
        self.main_layout.addLayout(self.id_layout)

        # 番剧ID
        self.anime_id_layout = QtWidgets.QHBoxLayout()
        self.label_anime_id = QtWidgets.QLabel(PlatformPurchaseBox)
        self.label_anime_id.setObjectName("label_anime_id")
        self.anime_id_layout.addWidget(self.label_anime_id)
        self.anime_id_edit = QtWidgets.QLineEdit(PlatformPurchaseBox)
        self.anime_id_edit.setClearButtonEnabled(True)
        self.anime_id_edit.setObjectName("anime_id_edit")
        self.anime_id_layout.addWidget(self.anime_id_edit)
        self.main_layout.addLayout(self.anime_id_layout)

        # 按钮布局
        self.button_layout = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton(PlatformPurchaseBox)
        self.ok_button.setObjectName("ok_button")
        self.button_layout.addWidget(self.ok_button, alignment=QtCore.Qt.AlignCenter)
        self.cancel_button = QtWidgets.QPushButton(PlatformPurchaseBox)
        self.cancel_button.setObjectName("cancel_button")
        self.button_layout.addWidget(self.cancel_button, alignment=QtCore.Qt.AlignCenter)
        self.main_layout.addLayout(self.button_layout)

        self.retranslateUi(PlatformPurchaseBox)
        QtCore.QMetaObject.connectSlotsByName(PlatformPurchaseBox)

    def retranslateUi(self, PlatformPurchaseBox):
        _translate = QtCore.QCoreApplication.translate
        PlatformPurchaseBox.setWindowTitle(_translate("PlatformPurchaseBox", "添加or删除平台购入记录"))
        self.msg.setText(_translate("PlatformPurchaseBox", "请输入购入记录的信息："))
        self.label_platform_id.setText(_translate("PlatformPurchaseBox", "平台ID"))
        self.label_anime_id.setText(_translate("PlatformPurchaseBox", "番剧ID"))
        self.ok_button.setText(_translate("PlatformPurchaseBox", "确定"))
        self.cancel_button.setText(_translate("PlatformPurchaseBox", "取消"))

class PlatformPurchase:
    """平台购入记录的实体类"""
    def __init__(self):
        self.platform_id = ""
        self.anime_id = ""

    def checkInfo(self):
        """检查购入记录信息是否完整"""
        if not self.platform_id:
            return False, "平台ID不能为空"
        if not self.anime_id:
            return False, "番剧ID不能为空"
        return True, "数据完整"


class PlatformPurchaseBox(QWidget):
    """平台购入记录编辑盒 - 基类"""
    def __init__(self):
        super().__init__()
        self.dialog = QDialog()
        window = Ui_PlatformPurchaseBox()
        window.setupUi(self.dialog)
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        # 获取 UI 元素
        self.platform_id_edit = window.platform_id_edit  # 平台ID
        self.anime_id_edit = window.anime_id_edit  # 番剧ID
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

    def applyToPlatformPurchase(self, platform_purchase):
        """将输入框的值应用到购入记录对象中"""
        platform_purchase.platform_id = self.platform_id_edit.text().strip()
        platform_purchase.anime_id = self.anime_id_edit.text().strip()

    def onFinished(self):
        """子类实现此方法以定义完成逻辑"""
        return False


class AddPlatformPurchaseBox(PlatformPurchaseBox):  # 继承自 PlatformPurchaseBox
    purchase_added = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.purchase = PlatformPurchase()  # 创建 PlatformPurchase 实例
        self.setTitle("新增平台购入记录")
        self.setMsg("请输入平台购入记录的信息")
        self.setButton("新增", "取消")

    def onFinished(self):
        """新增平台购入记录的逻辑"""
        self.applyToPlatformPurchase(self.purchase)
        check, info = self.purchase.checkInfo()
        if check:
            sql_check = PlatformPurchaseManager.add_purchase(
                platform_id=self.purchase.platform_id,
                anime_id=self.purchase.anime_id
            )
            if sql_check:
                QMessageBox.information(self.dialog, "成功", "购入记录新增成功！")
                self.purchase_added.emit()
                return True
            else:
                QMessageBox.warning(self.dialog, "失败", "购入记录新增失败！（可能是记录已存在或平台ID/番剧ID不存在,数据库插入失败）")
                return False
        else:
            QMessageBox.warning(self.dialog, "失败", info)
            return False

# 继承自PlatformPurchaseBox

class DeletePlatformPurchaseBox(PlatformPurchaseBox):
    purchase_deleted = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.purchase = PlatformPurchase()  # 创建 PlatformPurchase 实例
        self.setTitle("删除平台购入记录")
        self.setMsg("请输入要删除的购入记录信息（平台id和番剧id都要输入）")
        self.setButton("删除", "取消")

    def onFinished(self):
        """删除平台购入记录的逻辑"""
        self.applyToPlatformPurchase(self.purchase)
        check, info = self.purchase.checkInfo()
        print(check)
        if check:
            if not PlatformPurchaseManager.get_records(
                    platform_id=self.purchase.platform_id,
                    anime_id=self.purchase.anime_id
            ):
                QMessageBox.warning(self.dialog, "失败", "购入记录不存在！")
                return False
            sql_check = PlatformPurchaseManager.delete_purchase(
                platform_id=self.purchase.platform_id,
                anime_id=self.purchase.anime_id
            )
            if sql_check:
                QMessageBox.information(self.dialog, "成功", "购入记录删除成功！")
                self.purchase_deleted.emit()
                return True
            else:
                QMessageBox.warning(self.dialog, "失败", "购入记录删除失败！（数据库删除失败）")
                return False
        else:
            QMessageBox.warning(self.dialog, "失败", info)
            return False

