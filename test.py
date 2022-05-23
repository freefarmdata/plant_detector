import cv2
import numpy as np

from lib.denoise import denoise
from lib.contour import find_contours, draw_contour
from lib.pixel_mass import get_pixel_mass
from lib.model import Model


if __name__ == "__main__":

    model = Model()
    model.save('./model.json')

    print(model)

    image_file = './images/plants.jpg'
    original_image = cv2.imread(image_file)

    denoised_mask = denoise(
        original_image,
        lower_color=np.array([model.lower_color]),
        upper_color=np.array([model.upper_color]),
        blur_kernel=model.blur_kernel,
        dilate_kernel=model.dilate_kernel,
        denoise_temp_size=model.denoise_temp_size,
        denoise_window_size=model.denoise_window_size,
        denoise_strength=model.denoise_strength
    )

    contours = find_contours(denoised_mask, bbox_min_area=model.bbox_min_area)

    for contour in contours:
        mass = get_pixel_mass(denoised_mask, contour['contour'])
        draw_contour(original_image, contour['contour'], contour['bbox'], mass)

    cv2.imshow('window', original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()