import cv2
from DicomDataset import DicomDataset
from PyQt5.QtWidgets import QMessageBox
from DicomProcessing import DicomProcessing

class Controller(object):

    def __init__(self, view):
        self.view = view
        self.dicom_reader = DicomDataset()
        self.dicom_processing = DicomProcessing()
        self.enable_segmentation = False

    def load_new_patient(self, directory):
        if self.dicom_reader.read_dicom_dataset(directory):
            self.view.browse_slider_initialization(self.dicom_reader.get_dataset_size())
            self.view.segmentation_slider_initialization(self.dicom_reader.get_dataset_max_value())
            self.view.update_current_image(self.dicom_reader.get_current_image())
            self.view.toggle_rendering_button(True)
            self.view.toggle_rendering_tools(False)
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

    def adjust_segmentation(self, value):
        self.dicom_processing.set_segmentation_threshold(value)

    def change_current_image(self, index):
        self.dicom_reader.set_current_image_index(index)
        image = self.dicom_reader.get_current_image()
        if self.enable_segmentation:
            image = self.dicom_processing.segmentation(image)
        self.view.update_current_image(image)
