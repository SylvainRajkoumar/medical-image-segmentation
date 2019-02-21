import cv2

class DicomProcessing(object):

    def __init__(self):
        self.segmentation_threshold = 0

    def segmentation(self, image):
        # Voir adaptativeThresold à la place
        ret, mask = cv2.threshold(image, self.segmentation_threshold, 65535, cv2.THRESH_BINARY)

        ellipsekernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        mask = cv2.erode(mask, ellipsekernel, iterations = 1)
        mask = cv2.dilate(mask, ellipsekernel, iterations = 1)
        
        segmented_image = cv2.bitwise_and(image, mask)
        return segmented_image

    def set_segmentation_threshold(self, value):
        self.segmentation_threshold = value