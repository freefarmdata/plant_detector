import cv2
import numpy as np

def denoise(
    image,
    lower_color=np.array([[55, 20, 20]]),
    upper_color=np.array([[80, 255, 255]]),
    denoise_temp_size=50,
    denoise_window_size=50,
    denoise_strength=20,
    blur_kernel=(5, 5),
    dilate_kernel=(5, 5)
):

    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    green_mask = cv2.inRange(hsv_image, lower_color, upper_color)
    denoise_mask = cv2.cvtColor(green_mask, cv2.COLOR_GRAY2RGB)
    denoise_mask = cv2.fastNlMeansDenoisingColored(
        denoise_mask,
        None,
        denoise_temp_size,
        denoise_window_size,
        denoise_strength,
        15
    )
    denoise_mask = cv2.blur(denoise_mask, blur_kernel, cv2.BORDER_DEFAULT) 
    denoise_mask = cv2.dilate(denoise_mask, np.ones(dilate_kernel, 'uint8'), iterations=1)
    denoise_mask = cv2.cvtColor(denoise_mask, cv2.COLOR_RGB2GRAY)

    return denoise_mask