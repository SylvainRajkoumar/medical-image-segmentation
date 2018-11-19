import cv2



class DicomProcessing(object):

    def __init__(self):
        self.segmentation_threshold = 0

    def segmentation(self, image):
        ret, segmented_image = cv2.threshold(image, self.segmentation_threshold, 65535, cv2.THRESH_BINARY)
        ellipsekernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        segmented_image = cv2.erode(segmented_image, ellipsekernel, iterations = 1)
        segmented_image = cv2.dilate(segmented_image, ellipsekernel, iterations = 1)
        return segmented_image

    def set_segmentation_threshold(self, value):
        self.segmentation_threshold = value