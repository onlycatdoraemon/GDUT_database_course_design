from sql_manager import PublisherManager
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox

class Ui_PublisherBox(object):
    def setupUi(self, PublisherBox):
        PublisherBox.setObjectName("PublisherBox")
        PublisherBox.setWindowIcon(QtGui.QIcon("./picture/icon_4.png"))
        PublisherBox.resize(500, 300)

        # 主布局
        self.main_layout = QtWidgets.QVBoxLayout(PublisherBox)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # 提示信息
        self.msg = QtWidgets.QLabel(PublisherBox)
        self.msg.setObjectName("msg")
        self.main_layout.addWidget(self.msg, alignment=QtCore.Qt.AlignCenter)

        # 出版社ID
        self.id_layout = QtWidgets.QHBoxLayout()
        self.label_id = QtWidgets.QLabel(PublisherBox)
        self.label_id.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_id.setObjectName("label_id")
        self.id_layout.addWidget(self.label_id)
        self.id_edit = QtWidgets.QLineEdit(PublisherBox)
        self.id_edit.setClearButtonEnabled(True)
        self.id_edit.setObjectName("id_edit")
        self.id_layout.addWidget(self.id_edit)
        self.main_layout.addLayout(self.id_layout)

        # 出版社名称
        self.name_layout = QtWidgets.QHBoxLayout()
        self.label_name = QtWidgets.QLabel(PublisherBox)
        self.label_name.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_name.setObjectName("label_name")
        self.name_layout.addWidget(self.label_name)
        self.name_edit = QtWidgets.QLineEdit(PublisherBox)
        self.name_edit.setClearButtonEnabled(True)
        self.name_edit.setObjectName("name_edit")
        self.name_layout.addWidget(self.name_edit)
        self.main_layout.addLayout(self.name_layout)

        # 按钮布局
        self.button_layout = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton(PublisherBox)
        self.ok_button.setObjectName("ok_button")
        self.button_layout.addWidget(self.ok_button, alignment=QtCore.Qt.AlignCenter)
        self.cancel_button = QtWidgets.QPushButton(PublisherBox)
        self.cancel_button.setObjectName("cancel_button")
        self.button_layout.addWidget(self.cancel_button, alignment=QtCore.Qt.AlignCenter)
        self.main_layout.addLayout(self.button_layout)

        self.retranslateUi(PublisherBox)
        QtCore.QMetaObject.connectSlotsByName(PublisherBox)

    def retranslateUi(self, PublisherBox):
        _translate = QtCore.QCoreApplication.translate
        PublisherBox.setWindowTitle(_translate("PublisherBox", "添加or删除出版社信息"))
        self.msg.setText(_translate("PublisherBox", "请输入出版社的信息："))
        self.label_id.setText(_translate("PublisherBox", "出版社ID"))
        self.label_name.setText(_translate("PublisherBox", "  名称  "))
        self.ok_button.setText(_translate("PublisherBox", "确定"))
        self.cancel_button.setText(_translate("PublisherBox", "取消"))

class Publisher:
    def __init__(self):
        self.id = ""
        self.name = ""
    def checkInfo(self):
        """检查出版社信息是否完整"""
        if not self.id:
            return False, "出版社ID不能为空"
        if not self.name:
            return False, "名称不能为空"
        return True, "数据完整"

class PublisherBox(QWidget):
    """出版社信息编辑盒 - 基类"""
    def __init__(self):
        super().__init__()
        self.dialog = QDialog()
        window = Ui_PublisherBox()
        window.setupUi(self.dialog)
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        # 获取 UI 元素
        self.id_edit = window.id_edit  # 出版社ID
        self.name_edit = window.name_edit  # 出版社名称
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

    def applyToPublisher(self, publisher):
        """将输入框的值应用到出版社对象中"""
        publisher.id = self.id_edit.text().strip()
        publisher.name = self.name_edit.text().strip()

    def onFinished(self):
        """子类实现此方法以定义完成逻辑"""
        return False

class AddPublisherBox(PublisherBox):  # 继承自 PublisherBox
    publisher_added = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.publisher = Publisher()
        self.setTitle("新增出版社信息")
        self.setMsg("请输入出版社信息：")
        self.setButton("新增", "取消")

    def onFinished(self):
        """新增出版社逻辑"""
        self.applyToPublisher(self.publisher)
        check, info = self.publisher.checkInfo()
        if check:
            sql_check = PublisherManager.add_publisher(
                publisher_id=self.publisher.id,
                name=self.publisher.name,
            )
            if sql_check:
                QMessageBox.information(self.dialog, "成功", "出版社信息新增成功！")
                self.publisher_added.emit()
                return True
            else:
                QMessageBox.warning(self.dialog, "失败", "新增失败（数据库新增失败，可能ID已存在）！")
                return False
        else:
            QMessageBox.warning(self.dialog, "信息不完整", info)
            return False

class DeletePublisherBox(PublisherBox):
    publisher_deleted = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.publisher = Publisher()
        self.setTitle("删除出版社信息")
        self.setMsg("请输入要删除的出版社ID或名称")
        self.setButton("删除", "取消")

    def onFinished(self):
        """删除逻辑"""
        publisher_id = self.id_edit.text().strip()
        publisher_name = self.name_edit.text().strip()
        if not publisher_id and not publisher_name:
            self.setMsg("大佬啊，出版社ID或名字至少输一个")
            return False

        if publisher_id:
            if not PublisherManager.get_publisher_by_id(publisher_id):
                QMessageBox.warning(self.dialog, "失败", "该出版商ID不存在")
                return False
            sql_check = PublisherManager.delete_publisher_by_id(publisher_id)
        else:
            if not PublisherManager.get_publishers_by_name(publisher_name):
                QMessageBox.warning(self.dialog, "失败", "该出版商名称不存在")
                return False
            sql_check = PublisherManager.delete_publisher_by_name(publisher_name)

        if sql_check:
            QMessageBox.information(self.dialog, "成功", "出版社信息删除成功！")
            self.publisher_deleted.emit()
            return True
        else:
            QMessageBox.information(self.dialog, "失败", "删除失败（数据库删除失败）")
            return False

class ChangePublisherBox(PublisherBox):  # 继承自 PublisherBox
    publisher_changed = pyqtSignal()

    def __init__(self):
        super().__init__()  # 调用 PublisherBox 的构造函数
        self.publisher = Publisher()  # 创建 Publisher 实例

        # 设置窗口标题和按钮文本
        self.setTitle("修改出版社信息")
        self.setMsg("请输入要修改的出版社信息(至少输入ID)：")
        self.setButton("修改", "取消")

    def onFinished(self):
        """修改出版社的逻辑"""
        publisher_id = self.id_edit.text().strip()
        publisher_name = self.name_edit.text().strip()

        if not publisher_id:
            QMessageBox.warning(self.dialog, "失败", "改出版社信息好歹输个ID吧，不然怎么改啊")
            return False
        if not PublisherManager.get_publisher_by_id(publisher_id):
            QMessageBox.warning(self.dialog, "失败", "该出版社ID不存在")
            return False
        # 更新出版社信息
        sql_check = PublisherManager.update_publisher(
            publisher_id=publisher_id,
            name=publisher_name,
        )
        if sql_check:
            QMessageBox.information(self.dialog, "成功", "出版社信息修改成功！")
            self.publisher_changed.emit()  # 发射信号
            return True
        else:
            QMessageBox.warning(self.dialog, "失败", "出版社信息修改失败（数据库修改失败）！")
            return False
