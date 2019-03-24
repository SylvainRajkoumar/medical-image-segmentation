import os
import cv2
import numpy as np
import vtk
from shutil import copyfile
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap
from RenderingView import RenderingView
from Controller import Controller


class View(QMainWindow):

    def __init__(self):
        super(View, self).__init__()
        loadUi('view.ui', self)
        self.show()
        self.control = None
        self.rendering_view = RenderingView()
        self.display_layout.addWidget(self.rendering_view)

        self.ui_initialization()

    def set_control(self, controller):
        self.control = controller
        self.signal_slot_initialization()

    def signal_slot_initialization(self):
        self.both_view_button.clicked.connect(self.change_display_visibility)
        self.original_view_button.clicked.connect(self.change_display_visibility)
        self.rendering_view_button.clicked.connect(self.change_display_visibility)
        self.load_folder_button.clicked.connect(self.get_directory)
        self.browse_slider.valueChanged.connect(self.handle_browse_slider)
        self.rendering_button.clicked.connect(self.vtk_rendering)
        self.segmentation_checkbox.clicked.connect(self.control.toggle_segmentation)
        self.segmentation_threshold_slider.valueChanged.connect(self.handle_segmentation_slider)
        self.reset_camera_button.clicked.connect(self.rendering_view.reset_camera)
        self.connectivity_button.clicked.connect(self.connectivity)
        self.centerline_button.clicked.connect(self.centerline)
        self.arter_button.clicked.connect(self.arter_type)

    def centerline(self):
        os.chdir("C:/Users/Sylvain/Anaconda3/envs/medical_segmentation/Lib/site-packages/vmtk")
        os.system("python vmtksurfacereader.py -ifile result.stl --pipe vmtkcenterlines.py --pipe vmtkrenderer.py --pipe vmtksurfaceviewer.py -opacity 0.10 --pipe vmtksurfaceviewer.py -i @vmtkcenterlines.o -array MaximumInscribedSphereRadius --pipe vmtksurfaceviewer.py -i @vmtkcenterlines.o")
    
    def arter_type(self):
        os.chdir("C:/Users/Sylvain/Anaconda3/envs/medical_segmentation/Lib/site-packages/vmtk")
        os.system("python vmtksurfacereader.py -ifile result.stl --pipe vmtkcenterlines.py --pipe vmtkpointsplitextractor.py -ofile centerlinespoints.dat")
    

    def connectivity(self):
        copyfile("D:/projet-medical/medical-image-segmentation/extracted.stl", 
        "C:/Users/Sylvain/Anaconda3/envs/medical_segmentation/Lib/site-packages/vmtk/extracted.stl")
        os.chdir("C:/Users/Sylvain/Anaconda3/envs/medical_segmentation/Lib/site-packages/vmtk")
        os.system("python vmtksurfaceconnectivity.py -ifile extracted.stl --pipe vmtksurfaceviewer.py -ofile result.stl")
    
    def vtk_rendering(self):
        self.rendering_view.reset()
        foldername = self.control.save_segmentation()
        self.rendering_view.load_dicom(foldername)

    def ui_initialization(self):
        self.toggle_browse_tools(False)
        self.toggle_rendering_button(False)
        self.toggle_rendering_tools(False)
        self.rendering_view.setVisible(False)
        self.original_view_button.setChecked(True)
        self.toggle_segmentation_checkbox(False)
        self.toggle_segmentation_slider(False)

    def toggle_segmentation_slider(self, boolean):
        self.segmentation_threshold_label.setVisible(boolean)
        self.segmentation_threshold_slider.setVisible(boolean)

    def toggle_browse_tools(self, boolean):
        self.image_number_label.setVisible(boolean)
        self.browse_slider.setVisible(boolean)

    def toggle_segmentation_checkbox(self, boolean):
        self.segmentation_checkbox.setVisible(boolean)

    def toggle_rendering_tools(self, boolean):
        self.reset_camera_button.setVisible(boolean)

    def toggle_rendering_button(self, boolean):
        self.connectivity_button.setVisible(boolean)
        self.centerline_button.setVisible(boolean)
        self.arter_button.setVisible(boolean)
        self.rendering_button.setVisible(boolean)

    @pyqtSlot()
    def handle_browse_slider(self):
        image_number = self.browse_slider.value()
        self.control.change_current_image(image_number)
        self.image_number_label.setText("Image Number : {}".format(image_number))

    @pyqtSlot()
    def handle_segmentation_slider(self):
        slider_value = self.segmentation_threshold_slider.value()
        self.control.adjust_segmentation(slider_value)
        self.rendering_view.set_rendering_threshold(slider_value)
        self.segmentation_threshold_label.setText("Segmentation Threshold : {}".format(slider_value))
    
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

    @pyqtSlot()
    def get_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Choose a folder")
        if(os.path.exists(directory)):
            if self.control.load_new_patient(directory):
                self.rendering_view.load_dicom(directory)
                self.rendering_view.set_rendering_threshold(0)
                self.toggle_segmentation_checkbox(True)
                self.toggle_rendering_button(True)
                self.toggle_rendering_tools(True)
                self.toggle_segmentation_slider(True)

    def browse_slider_initialization(self, dataset_size):
        self.browse_slider.setRange(0, dataset_size - 1)
        self.browse_slider.setValue(0)
        self.toggle_browse_tools(True)

    def segmentation_slider_initialization(self, max_value):
        self.segmentation_threshold_slider.setRange(0, max_value)
        self.segmentation_threshold_slider.setValue(0)

    def update_original_view(self, image):
        pixmap = self.convert_to_grayscale_pixmap(image)
        self.original_image_display.setPixmap(pixmap.scaled(self.original_image_display.width(), self.original_image_display.height(), Qt.KeepAspectRatio))

    def convert_to_grayscale_pixmap(self, image):
        height, width = image.shape
        tempArray = np.zeros(image.shape, dtype=np.uint16)
        tempArray = cv2.normalize(image, dst=None, alpha=0, beta=65536, norm_type=cv2.NORM_MINMAX)
        temp = (tempArray/256).astype('uint8')
        qImg = QImage(temp, width, height, width, QImage.Format_Grayscale8)

        return QPixmap.fromImage(qImg)
