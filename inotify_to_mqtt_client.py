import json
import time
import os
from datetime import datetime

import cv2
import numpy as np
import paho.mqtt.client as mqtt
from inotify_simple import flags

from lib.denoise import denoise
from lib.contour import find_contours
from lib.pixel_mass import get_pixel_mass
from lib.watcher import DirWatcher
from lib.model import Model

if __name__ == "__main__":

    publish_topic = 'test'
    camera_name = 'testcam'
    raw_file = './raw_results.txt'
    watch_directory = './images'
    model_file_path = './model.json'
    mosquitto_broker = "127.0.0.1"
    mosquitto_port = 1883

    # mqtt_client = mqtt.Client()
    # mqtt_client.connect(mosquitto_broker, mosquitto_port, 60)
    # mqtt_client.loop_start()

    model = Model()
    model.load(model_file_path)
    model.save(model_file_path)

    #with DirWatcher(watch_directory, flags.CLOSE_WRITE) as watcher:
    #    for event in watcher.next(timeout=2):
    image_file = os.path.join(watch_directory, 'plants.jpg')
    if os.path.exists(image_file):
        timestamp = int(time.time())

        print(f'new image taken: {image_file} at {datetime.fromtimestamp(timestamp).isoformat()}')

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

        for index, contour in enumerate(contours):
            mass = get_pixel_mass(denoised_mask, contour['contour'])

            packet = {
                'image': image_file,
                'timestamp': timestamp,
                'camera': camera_name,
                'instance': index,
                'mass': mass
            }

            raw = {
                **packet,
                'contour': contour['contour'].tolist(),
                'bbox': contour['bbox'],
            }

            #mqtt_client.publish(publish_topic, json.dump(packet))

            with open(raw_file, 'a') as f:
                f.write(json.dumps(raw) + '\n')
    
    # mqtt_client.loop_stop()
    # mqtt_client.disconnect()

        
        

