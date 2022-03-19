import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import os
from os import listdir
import re
from cv2 import *



class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    # def __init__(self):
    #     super().__init__()
    # self._run_flag = True
    _run_flag = True

    def run(self):
        RTSP_URL = 'rtsp://127.0.0.1:8554/demo' 
        os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
         
        cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        print(dir(self._run_flag))
        self._run_flag = False
        self.wait()


# def start(self):
#     """Sets run flag to False and waits for thread to finish"""
#     self._run_flag = True
#     self.wait()

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("myui.ui", self)
        MainWindow.showMaximized(self)
        
        self.disply_width = 720
        self.display_height = 576
        # create the label that holds the image
        # self.label_7 = QLabel(self)
        # self.label_7.setObjectName("label_7")
        
        self.stiilcapture.clicked.connect(self.preview)
        # self.verticalLayout.addWidget(self.label_7)
        self.label.resize(self.disply_width, self.display_height)
        # print(self.label.image())

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()


    def preview(self):

        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # self.thread.change_pixmap_signal.connect(self.update_image)
        # self.stiilcapture.clicked.connect(self.startcapture)
        # self.thread.change_pixmap_signal.connect(self.test)
        # start the thread
        self.thread.start()


    def startcapture(self, event):
        # self.test1 = "true"
        # self.test(event)
        # print(dir(self.update_image))

        # self.thread.start()
        # event.accept()
        # print(dir(self.label))
        channels_count = 4
        # pixmap = self.label.grab(0, self._x, self._y, self._width, self._height)
        pixmap = self.label.grab(0)
        image = pixmap.toImage()
        s = image.bits().asstring(self._width * self._height * channels_count)
        arr = np.fromstring(s, dtype=np.uint8).reshape((self._height, self._width, channels_count)) 
        print(arr)


    @pyqtSlot(np.ndarray)

    # def onClick(self):
    #     cap = cv2.VideoCapture(0)

    #     while (cap.isopened()):
    #         ret, frame =cap.read()
    #         if ret ==True:
    #             print("here")
    #             self.displayImage(frame,1)
    #             cv2.waitkey()

    #             if(self.logic==2):
    #                 self.imwriter('c:/test/test/%s.png'%(self.value), frame)
    #                 self.logic=1
    #                 self.TExt.settext("test")
    #         else:
    #             print("return not found")

    #     cap.release()


    # def displayImage(self, img,)
    
       
    def test(self):
        # get the filenames in directory
        basepath = "C:\\Users\\91787\\Desktop\\ff\\rtsp_recorder\\images\\"
        files = listdir(basepath)
        # print(files)
               
        
        # for files in os.listdir(basepath):
        #     if files.endswith(".png"):
        #         # i = Image.open(f)
        #         # fn, fext = os.path.splitext(files)
        #         fn = max(files)
        #         print(fn)
        #     # declare valid filtypes
        #     # valid_image_extensions = [".jpg", ".png",] 
        
        print(self.label.Pixmap)
        # if not os.path.exists(basepath+"pic000.png"):
        #     # print(files)
        #     cv2.imwrite(basepath+"pic%s.png" % str("000"),qt_img)
        #     # print("pic%s.png" % i)
        # else:
        #     file = max(files)
        #     # print(file)
        #     fn, fext = os.path.splitext(file)
        #     # i = int(re.match('.*?([0-9]+)$', fn).group(1))
        #     i = re.findall('^.*-([0-9]+)$',fn)
        #     i2 = str(i)
        #     i2 +=1
        #     print(i)
        #     cv2.imwrite(basepath+"pic%s.png" % i2,qt_img)

    
        # for name in files:
        #         # check if it is a valid filetype
        #         filename, file_extension = os.path.splitext(name)
        #         if not filename and file_extension:
                    
        #         if file_extension in valid_image_extensions:
        #                 # create a folder for this image
        #                 path = basepath+filename
        #                 if not os.path.exists(path):
        #                         os.makedirs(path)
        #                 # load image in grayscale
        #                 cv2.imwrite(basepath+name+'.png',0)
                        # threshold image
                        # print(type(qt_img))
                        # cv2.imwrite('color_img%s.png'%(self.value), qt_img)
                        # # cv2.imshow("image", qt_img)
                        # cv2.waitKey()


    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        # imwrite("GeeksForGeeks.png", cv_img)
        # print(cv_img)
        self.label.setPixmap(qt_img)
        # self.test(cv_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        # print(rgb_image)
        return QPixmap.fromImage(p)




app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()