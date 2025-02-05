import sys
import cv2
import time
import rospy
import threading
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QDialog, QMessageBox
from lab_config_proxy import LabConfigProxy
from ui import *
import add_color_dialog
from sensor_msgs.msg import Image
import camera_thread

class MainWindow(QWidget, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.last_range_max = [999, 999, 999]
        self.last_range_min = [999, 999, 999]
        ip = "127.0.0.1"
        
        self.lab_config_proxy = LabConfigProxy(host=ip, port=9090)
        self.lab_config_proxy.enter_func()

        self.comboBox_color.currentTextChanged.connect(self.set_slider_by_combobox)
        self.horizontalSlider_LMax.valueChanged.connect(lambda value: self.label_LMax.setNum(value))
        self.horizontalSlider_LMin.valueChanged.connect(lambda value: self.label_LMin.setNum(value))
        self.horizontalSlider_AMax.valueChanged.connect(lambda value: self.label_AMax.setNum(value))
        self.horizontalSlider_AMin.valueChanged.connect(lambda value: self.label_AMin.setNum(value))
        self.horizontalSlider_BMax.valueChanged.connect(lambda value: self.label_BMax.setNum(value))
        self.horizontalSlider_BMin.valueChanged.connect(lambda value: self.label_BMin.setNum(value))
        self.pushButton_labWrite.clicked.connect(self.save_ranges_to_disk)
        self.pushButton_AddColor.clicked.connect(self.add_color)
        self.pushButton_exit.clicked.connect(self.exit)
        self.update_color_names()
        self.range_update_timer = threading.Timer(0.05, self.update_current_range)
        self.range_update_timer.setDaemon(True)
        self.range_update_timer.start()

        self.ros_camera = camera_thread.ROS_Camera('/lab_config_manager/image_result')
        self.ros_camera.raw_data.connect(self.show_image)
        self.ros_camera.enter()
        self.ros_camera.start()

    def show_image(self, image):
        image = cv2.resize(image, (400, 600), interpolation=cv2.INTER_NEAREST) 
        image_o = image.copy()[:300, :]
        image_p = image.copy()[300:, :]
        image_ = np.hstack((image_o, image_p))
        qimage = QImage(image_.data, 800, 300, QImage.Format_RGB888)
        self.label_orign.setPixmap(QPixmap.fromImage(qimage))

    # 窗口退出(window exit)
    def closeEvent(self, e):        
        result = QMessageBox.question(self,
                                    "关闭窗口提醒",
                                    "exit?",
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        if result == QMessageBox.Yes:
            self.lab_config_proxy.exit_func()
            self.ros_camera.exit()
            QWidget.closeEvent(self, e)
        else:
            e.ignore()

    def apply_current_range(self):
        rsl = self.lab_config_proxy.apply_current_range(self.comboBox_color.currentText())
        if rsl['success']:
            QMessageBox.information(self, "Apply color range", "Successed!")
        else:
            QMessageBox.information(self, "Apply color range", "Failed")

    def save_ranges_to_disk(self):
        self.lab_config_proxy.apply_current_range(self.comboBox_color.currentText())
        rsl = self.lab_config_proxy.save_ranges_to_disk()
        if rsl['success']:
            QMessageBox.information(self, "Save to disk", "Successed!")
        else:
            QMessageBox.information(self, "Save to disk", "Failed")

    def add_color(self):
        dialog = QDialog()
        dialog_ui = add_color_dialog.Ui_Dialog()
        dialog_ui.setupUi(dialog)

        def get_color_name():
            color_name = dialog_ui.lineEdit.text()
            self.lab_config_proxy.apply_current_range(color_name)
            self.comboBox_color.addItem(color_name)
            self.comboBox_color.setCurrentText(color_name)
            dialog.close()

        dialog_ui.pushButton_ok.clicked.connect(get_color_name)
        dialog_ui.pushButton_cancel.clicked.connect(dialog.close)
        dialog.exec_()

    def update_current_range(self):
        range_max = list((int(n) for n in (self.label_LMax.text(), self.label_AMax.text(), self.label_BMax.text())))
        range_min = list((int(n) for n in (self.label_LMin.text(), self.label_AMin.text(), self.label_BMin.text())))
        if not (range_max == self.last_range_max and range_min == self.last_range_min):
            self.lab_config_proxy.set_current_range(range_min, range_max)
            self.last_range_max = range_max
            self.last_range_min = range_min
        self.range_update_timer = threading.Timer(0.05, self.update_current_range)
        self.range_update_timer.start()

    def update_color_names(self):
        names = self.lab_config_proxy.get_all_color_name()
        names.sort()
        self.comboBox_color.addItems(names)

    def set_slider_states(self, range_min, range_max):
        self.horizontalSlider_LMin.setSliderPosition(range_min[0])
        self.horizontalSlider_AMin.setSliderPosition(range_min[1])
        self.horizontalSlider_BMin.setSliderPosition(range_min[2])
        self.horizontalSlider_LMax.setSliderPosition(range_max[0])
        self.horizontalSlider_AMax.setSliderPosition(range_max[1])
        self.horizontalSlider_BMax.setSliderPosition(range_max[2])

    def set_slider_by_combobox(self, msg):
        rsl = self.lab_config_proxy.get_range_by_name(msg)
        self.set_slider_states(rsl['min'], rsl['max'])
        self.lab_config_proxy.set_current_range(rsl['min'], rsl['max'])

    def exit(self):
        self.lab_config_proxy.exit_func()
        self.ros_camera.exit()
        sys.exit()

if __name__ == "__main__":
    rospy.init_node('lab_node')
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
