from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
import time
import sys
from package.ui import AppLayout
from pathlib import Path
# import re
# import datetime
import glob
import logging
# import json
from bs4 import BeautifulSoup
# from urllib.request import Request,urlopen
from PyQt5 import QtWebEngineWidgets as qtwe
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

class PytureApplication(QtWidgets.QMainWindow, AppLayout.Ui_MainWindow):

    def __init__(self, parent=None):
        super(PytureApplication, self).__init__(parent)
        self.setupUi(self)
        # self.webview = qtwe.QWebEngineView()
        self.base_path = Path.cwd()

        #holder for the cureent list of images
        self.image_reel = []
        self.cur_image = 0


        #init the u
        self.files = []
        self.init_application()
        self.actionLoad.triggered.connect(self.load_directory)



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


    def get_scaled_image_at_index(self, inx):
        og = QtGui.QPixmap(self.image_reel[inx])
        og_size = og.size()
        scaled = og.scaled(QtCore.QSize(self.centralwidget.width(),self.centralwidget.height()), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        return scaled


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
            # print(search_path)
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

        if QMouseEvent.x() < win_rect/2:
          self.prev_image()
        else:
          self.next_image()
          

    def resizeEvent(self, event):
        logger.debug(f"{str(self.width())} x {str(self.height())}")
        logger.debug(f"Size:{str(event.size())}")


        if len(self.image_reel) > 0:
            self.get_scaled_image_and_display()

        return super(PytureApplication, self).resizeEvent(event)
