import os

import cv2
import numpy as np 

import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from RenderingView import RenderingView
from Controller import Controller

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap


class View(QMainWindow):

    def __init__(self):
        super(View, self).__init__()
        loadUi('view.ui', self)
        self.show()
        self.control = None
        self.rendering_view = RenderingView()
        self.horizontalLayout_3.addWidget(self.rendering_view)

        self.ui_initialization()
        self.signal_slot_initialization()

    def set_control(self, controller):
        self.control = controller

    def signal_slot_initialization(self):
        self.both_view_button.clicked.connect(self.change_display_visibility)
        self.original_view_button.clicked.connect(self.change_display_visibility)
        self.rendering_view_button.clicked.connect(self.change_display_visibility)
        self.load_folder_button.clicked.connect(self.get_directory)
        self.browse_slider.valueChanged.connect(self.slider_moved)
        self.rendering_button.clicked.connect(self.update_rendering)

    def update_rendering(self):
        self.rendering_view.update_rendering_view()

    def ui_initialization(self):
        self.toggle_browse_slider(False)
        self.toggle_rendering_button(False)
        self.toggle_rendering_tools(False)
        self.rendering_view.hide()
        self.original_view_button.setChecked(True)

    def toggle_browse_slider(self, boolean):
        self.browse_slider.setDisabled(not boolean)

    def toggle_rendering_tools(self, boolean):
        self.smooth_rendering_slider.setDisabled(not boolean)
        self.save_rendering_button.setDisabled(not boolean)
        self.reset_camera_button.setDisabled(not boolean)

    def toggle_rendering_button(self, boolean):
        self.rendering_button.setDisabled(not boolean)

    @pyqtSlot()
    def slider_moved(self):
        self.control.change_current_image(self.browse_slider.value())

    @pyqtSlot()
    def change_display_visibility(self):
        sender = self.sender()
        radio_button_name = sender.accessibleName()
        if(radio_button_name == 'both'):
            self.rendering_view.show()
            self.original_image_display.show()
        elif(radio_button_name == 'rendering'):
            self.original_image_display.hide()
            self.rendering_view.show()
        elif(radio_button_name == 'original'):
            self.rendering_view.hide()
            self.original_image_display.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        elif event.key() == Qt.Key_Escape:
            self.deleteLater()

    @pyqtSlot()
    def get_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Choose a folder")
        if(os.path.exists(directory)):
            if self.control.load_new_patient(directory):
                self.rendering_view.load_dicom(directory)

    def slider_initialization(self, datasetSize):
        self.browse_slider.setRange(0, datasetSize - 1)
        self.browse_slider.setValue(0)
        self.toggle_browse_slider(True)

    def update_current_image(self, image):
        pixmap = self.convert_to_grayscale_pixmap(image)
        self.original_image_display.setPixmap(pixmap.scaled(self.original_image_display.width(), self.original_image_display.height(), Qt.KeepAspectRatio))

    def convert_to_grayscale_pixmap(self, image):
        height, width = image.shape
        tempArray = np.zeros(image.shape, dtype=np.uint16)
        tempArray = cv2.normalize(image, dst=None, alpha=0, beta=65536, norm_type=cv2.NORM_MINMAX)
        temp = (tempArray/256).astype('uint8')
        qImg = QImage(temp, width, height, width, QImage.Format_Grayscale8)

        return QPixmap.fromImage(qImg)


    def a(self):
        #récupérer l'index de l'image à choisir (valeur du slider)
        #récupérer la valeur du seuillage (valeur du slider)
        #valeur checkbox (masque seuillage)
        #emettre un signal (à relier dans le controller)
        pass