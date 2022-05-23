import cv2
import imutils

# RETR_EXTERNAL
# RETR_LIST
# RETR_CCOMP
# RETR_TREE
# RETR_FLOODFILL

# CHAIN_APPROX_NONE
# CHAIN_APPROX_SIMPLE
# CHAIN_APPROX_TC89_L1
# CHAIN_APPROX_TC89_KCOS

def draw_contours(image, contours):
    for c in contours:
        contour = c['contour']
        bbox = c['bbox']
        cv2.drawContours(image, [contour], 0, color=(0, 0, 255), thickness=2)
        cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), color=(0, 0, 255), thickness=1)


def find_contours(
    mask,
    bbox_min_area=3000
):
    contours = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = imutils.grab_contours(contours)

    bbox_contours = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        bbox_contours.append({
            'bbox': [x, y, w, h],
            'contour': contour
        })

    def contour_sort(o):
        x, y, w, h = o['bbox']
        return [x, y]

    def contour_filter(o):
        x, y, w, h = o['bbox']
        return w*h > bbox_min_area

    bbox_contours = list(filter(contour_filter, bbox_contours))
    bbox_contours = sorted(bbox_contours, key=contour_sort)

    return bbox_contours
