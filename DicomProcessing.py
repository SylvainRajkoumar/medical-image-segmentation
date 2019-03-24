import cv2

class DicomProcessing(object):

    def __init__(self):
        self.segmentation_threshold = 0

    def segmentation(self, image):

        ret, thresholded_frame = cv2.threshold(image, self.segmentation_threshold, 65535, cv2.THRESH_BINARY)
        segmented_image = cv2.bitwise_and(image, thresholded_frame)

        return segmented_image

    def set_segmentation_threshold(self, value):
        self.segmentation_threshold = value