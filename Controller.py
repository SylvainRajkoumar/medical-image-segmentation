# Third-Party Libraries
import cv2
import numpy as np
from PyQt5.QtWidgets import QMessageBox

from DicomDataset import DicomDataset
from DicomProcessing import DicomProcessing
from utils.decorators import timeit
import pydicom
import os, glob, shutil


class Controller(object):

    def __init__(self, view):
        self.view = view
        self.dicom_reader = DicomDataset()
        self.dicom_processing = DicomProcessing()
        self.enable_segmentation = False

    @timeit
    def load_new_patient(self, directory):

        if self.dicom_reader.read_dicom_dataset(directory):
            self.view.browse_slider_initialization(self.dicom_reader.get_dataset_size())
            self.view.segmentation_slider_initialization(self.dicom_reader.get_dataset_max_value())
            self.update_current_image()
            return True
        
        #  A déplacer dans la vue
        warning = QMessageBox()
        warning.setWindowTitle("Error while loading DICOM files")
        warning.setText("Please make sure that only dicom files are in the selected folder")
        warning.setStandardButtons(QMessageBox.Ok)
        warning.exec()
        return False

    def toggle_segmentation(self):
        self.enable_segmentation = not self.enable_segmentation
        self.update_current_image()

    def adjust_segmentation(self, value):
        self.dicom_processing.set_segmentation_threshold(value)
        if self.enable_segmentation:
            self.update_current_image()

    def change_current_image(self, index):
        self.dicom_reader.set_current_image_index(index)
        self.update_current_image()

    def update_current_image(self):
        image = self.dicom_reader.get_current_image()
        if self.enable_segmentation:
            image = self.dicom_processing.segmentation(image)
        self.view.update_original_view(image)

    def save_segmentation(self):
        images, filenames, raw_data = self.dicom_reader.get_dataset()
        path = "segmented_images"
        if os.path.isdir('./' + path):
            shutil.rmtree('./' + path)
        os.mkdir(path)
        os.chdir('./' + path)

        for image, filename, raw in zip(images, filenames, raw_data):
            raw.PixelData = self.dicom_processing.segmentation(image)
            raw.Rows = 352
            raw.Colums = 308
            pydicom.dcmwrite(filename, raw)
        os.chdir('../')
        return path
