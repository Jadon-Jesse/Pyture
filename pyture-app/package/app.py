from PyQt5 import QtCore, QtGui, QtWidgets
import time
import sys
from package.ui import AppLayout
from pathlib import Path
# import re
# import datetime
import glob
import logging
# import json
# from bs4 import BeautifulSoup
# from urllib.request import Request,urlopen
# from PyQt5 import QtWebEngineWidgets as qtwe
import io
# import requests
# from PIL import Image

import random
import os

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    # handlers=handlers
)
logger = logging.getLogger("LOGGER_NAME")
app_icon = Path("logo.ico")


class PytureApplication(QtWidgets.QMainWindow, AppLayout.Ui_MainWindow):

    def __init__(self, parent=None):
        super(PytureApplication, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(str(app_icon)))
        
        # self.webview = qtwe.QWebEngineView()
        self.base_path = Path.cwd()

        #holder for the cureent list of images
        self.image_reel = []
        self.cur_image = 0

        self.autoPlay_on = False
        self.zooms = 0
        self.zoom_rate = 100

        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(False)
        self._timer.timeout.connect(self.next_image)

        #init the u
        self.files = []
        self.init_application()
        self.actionLoad.triggered.connect(self.load_directory)


    def on_context_menu(self, point):
        # show context menu
        self.popMenu.exec_(self.button.mapToGlobal(point))      



    def set_image_reel(self, images):
        #set the current image back to 0
        self.reset_current_image_pos()
        self.image_reel = images


    def reset_current_image_pos_to_len(self):
        self.cur_image = len(self.image_reel) - 1


    def reset_current_image_pos(self):
        self.cur_image = 0


    def inc_current_image_pos(self):
        self.cur_image += 1


    def dec_current_image_pos(self):
        self.cur_image -= 1


    def next_current_image(self):
        self.inc_current_image_pos()

        if self.cur_image >= len(self.image_reel):
            #if we are at the end of the image reel, loop back around
            self.reset_current_image_pos()


    def prev_current_image(self):
        self.dec_current_image_pos()

        if self.cur_image < 0:
            #if we are at the end of the image reel, loop back around
            self.reset_current_image_pos_to_len()


    def display_image(self, image):
        self.imageLbl.setPixmap(image)


    def get_scaled_image(self):
        logger.debug(f"c image {self.cur_image}")
        og = QtGui.QPixmap(self.image_reel[self.cur_image])
        og_size = og.size()
        scaled = og.scaled(QtCore.QSize(self.centralwidget.width(),self.centralwidget.height()), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        return scaled


    def get_scaled_image_and_display(self):
        self.display_image(self.get_scaled_image())


    def load_directory(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        options |= QtWidgets.QFileDialog.ShowDirsOnly
        diruploaded = QtWidgets.QFileDialog.getExistingDirectory(self, options=options)
        if diruploaded:
            dir_path = Path(diruploaded)

            #First check if there are any pics in the base path
            image_files = self.find_all_supported_image_files_in_path(dir_path)
            if len(image_files) > 0:
                self.set_image_reel(image_files)
                self.get_scaled_image_and_display()
            else:
                logger.debug("no images in selected dir")

            file_name = dir_path.name

            logger.debug(f"{dir_path} -- {file_name}")




    def next_image(self):
        if len(self.image_reel) > 0:
            #increase the current image pos properly
            self.next_current_image()

            #display the current image
            self.get_scaled_image_and_display()
        else:
            #No images found in reel, cant move
            logger.debug("No images in reel")


    def prev_image(self):
        if len(self.image_reel) > 0:

            self.prev_current_image()

            #display the current image
            self.get_scaled_image_and_display()
        else:
            #No images found in reel, cant move
            logger.debug("prev No images in reel")


    def find_all_supported_image_files_in_path(self, query_path):
        supported_exts = [
            "*.bmp",
            "*.gif",
            "*.jpg",
            "*.jpeg",
            "*.png",
            "*.pbm",
            "*.pgm",
            "*.ppm",
            "*.xbm",
            "*.xpm",
        ]

        supported_image_files = []

        for ext in supported_exts:
            search_ext = query_path.glob(ext)
            files = list(map(str, search_ext))
            supported_image_files.extend(files)
        return supported_image_files


    def init_application(self):
        #First check if there are any pics in the base path
        image_files = self.find_all_supported_image_files_in_path(self.base_path)
        if len(image_files) > 0:
            self.set_image_reel(image_files)
            self.get_scaled_image_and_display()
        else:
            logger.debug("no images in current dir")


    def mousePressEvent(self, QMouseEvent):
        logger.debug(QMouseEvent.pos())


    def mouseReleaseEvent(self, QMouseEvent):
        win_rect = self.width()
        logger.debug(QMouseEvent.button())

        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            logger.debug("left")
            if QMouseEvent.x() < win_rect/2:
              self.prev_image()
            else:
              self.next_image()

        elif QMouseEvent.button() == QtCore.Qt.RightButton:
            logger.debug("Right Click - open contect menu")


    def auto_next(self, interval):
        self._timer.start(interval)


    def resizeEvent(self, event):
        logger.debug(f"{str(self.width())} x {str(self.height())}")
        logger.debug(f"Size:{str(event.size())}")


        if len(self.image_reel) > 0:
            self.get_scaled_image_and_display()

        # return super(PytureApplication, self).resizeEvent(event)

    def contextMenuEvent(self, event):
        logger.debug(f"Context event")
        contextMenu = QtWidgets.QMenu(self)


        contextMenuAutoPlay = QtWidgets.QMenu("Start AutoPlay")
        autoStart_5s = contextMenuAutoPlay.addAction("5s")
        autoStart_30s = contextMenuAutoPlay.addAction("30s")
        autoStart_60s = contextMenuAutoPlay.addAction("60s")


        load_act = contextMenu.addAction("Load")
        contextMenu.addSeparator()

        autoPlay_start_menu = contextMenu.addMenu(contextMenuAutoPlay)
        autoPlay_stop_act = contextMenu.addAction("Stop AutoPlay")

        if self.autoPlay_on:
            autoPlay_stop_act.setEnabled(True)
            autoPlay_start_menu.setEnabled(False)
        else:
            autoPlay_stop_act.setEnabled(False)
            autoPlay_start_menu.setEnabled(True)


        contextMenu.addSeparator()

        quit_act = contextMenu.addAction("Quit")

        act = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if act == load_act:
            logger.debug("Load action")
            self.load_directory()

        elif act == autoStart_5s:
            logger.debug("Start 5s")
            self.autoPlay_on=True
            interval = 5 * 1000
            self._timer.start(interval)

        elif act == autoStart_30s:
            logger.debug("Start 30 ")
            self.autoPlay_on=True
            interval = 30 * 1000
            self._timer.start(interval)

        elif act == autoStart_60s:
            logger.debug("Start 60 ")
            self.autoPlay_on=True
            interval = 60 * 1000
            self._timer.start(interval)


        elif act == autoPlay_stop_act:
            logger.debug("STop Auto ")
            self.autoPlay_on=False
            self._timer.stop()



        elif act == quit_act:
            logger.debug("quit")
            self.close()


        # return super(PytureApplication, self).contextMenuEvent(event)





