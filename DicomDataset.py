import pydicom
import glob
import time
import os
import numpy as np


class DicomDataset(object):

    def __init__(self):
        object.__init__(self)
        self.dicom_dataset = None
        self.current_index = 0


    def read_dicom_dataset(self, folder_path):
        temp_dicom_dataset = []
        
        for path in os.listdir(folder_path):
            if os.path.join(folder_path, path).split(".")[-1] == "dcm":
                dicom = pydicom.dcmread(os.path.join(folder_path, path))
                temp_dicom_dataset.append(dicom.pixel_array)

        if temp_dicom_dataset:
            self.dicom_dataset = temp_dicom_dataset.copy()
            return True
        return False

    def get_current_image(self):
        return self.dicom_dataset[self.current_index]

    def set_current_image_index(self, newIndex):
        self.current_index = newIndex

    def get_dataset_size(self):
        return len(self.dicom_dataset)

    def get_dataset_max_value(self):
        return np.amax(self.dicom_dataset)

if __name__ == '__main__':
    a = DicomDataset()
    start = time.time()
    a.read_dicom_dataset("D:/Projet_3CT_Medical/Data_IRM/02-OS/")
    end = time.time()
    print(end - start)