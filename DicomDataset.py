import glob
import time
import os
import pydicom
import numpy as np
import vtk
from vtk.util import numpy_support
from utils.decorators import timeit


class DicomDataset(object):

    def __init__(self):
        object.__init__(self)
        self.dicom_dataset = None
        self.raw_dataset = None
        self.dataset_filename = None
        self.current_index = 0

    @timeit
    def read_dicom_dataset(self, folder_path):
        temp_dicom_dataset = []
        temp_dataset_filename = []
        temp_raw_dataset = []
        paths = os.listdir(folder_path)
  
        for path in paths:
            if os.path.join(folder_path, path).split(".")[-1] == "dcm":
                dicom = pydicom.dcmread(os.path.join(folder_path, path))

                temp_raw_dataset.append(dicom)
                temp_dataset_filename.append(path)
                temp_dicom_dataset.append(dicom.pixel_array)
        
        if temp_dicom_dataset:
            self.dicom_dataset = temp_dicom_dataset.copy()
            self.raw_dataset = temp_raw_dataset.copy()
            self.dataset_filename = temp_dataset_filename.copy()
            return True
        else:
            return False

    def get_current_image(self):
        return self.dicom_dataset[self.current_index]

    def set_current_image_index(self, newIndex):
        self.current_index = newIndex

    def get_dataset_size(self):
        return len(self.dicom_dataset)

    def get_dataset_max_value(self):
        return np.amax(self.dicom_dataset)
    
    def get_dataset(self):
        return self.dicom_dataset, self.dataset_filename, self.raw_dataset