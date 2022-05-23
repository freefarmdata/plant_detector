import cv2
import numpy as np

def get_pixel_mass(mask, contour):
    zero_mask = np.zeros(mask.shape, np.uint8)
    cv2.drawContours(zero_mask, [contour], 0, 255, -1)
    masked = cv2.bitwise_and(mask, mask, mask=zero_mask)
    total = np.count_nonzero(masked)
    return total