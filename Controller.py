import cv2
from DicomDataset import DicomDataset


class Controller(object):

    def __init__(self, view):
        self.view = view
        self.dicom_reader = DicomDataset()

    def load_new_patient(self, directory):
        if self.dicom_reader.read_dicom_dataset(directory):
            self.view.slider_initialization(self.dicom_reader.get_dataset_size())
            self.view.update_current_image(self.dicom_reader.get_current_image())
            self.view.toggle_rendering_button(True)
            self.view.toggle_rendering_tools(False)
        else:
            # QDialog
            print("Please make sure that only dicom files are in the selected folder")

    def change_current_image(self, index):
        self.dicom_reader.set_current_image_index(index)
        self.view.update_current_image(self.dicom_reader.get_current_image())

    def dicom_processing(self, index):
        pass