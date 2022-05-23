import json
import time
import os
from dataclasses import dataclass
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

@dataclass
class Config:

    publish_topic: str = 'test'
    camera_name: str = 'testcam'
    raw_file: str = './raw_results.txt'
    watch_directory: str = './images'
    model_file_path: str = './model.json'
    mosquitto_broker: str = "127.0.0.1"
    mosquitto_port: int = 1883


def process_image(model: Model, mqtt_client: mqtt.Client, config: Config, image_file: str):
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
            'camera': config.camera_name,
            'instance': index,
            'mass': mass
        }

        mqtt_client.publish(config.publish_topic, json.dump(packet))

        raw = {
            **packet,
            'contour': contour['contour'].tolist(),
            'bbox': contour['bbox'],
        }

        with open(config.raw_file, 'a') as f:
            f.write(json.dumps(raw) + '\n')


if __name__ == "__main__":

    config = Config()

    mqtt_client = mqtt.Client()
    mqtt_client.connect(config.mosquitto_broker, config.mosquitto_port, 60)
    mqtt_client.loop_start()

    model = Model()
    model.load(config.model_file_path)
    model.save(config.model_file_path)

    try:
        with DirWatcher(config.watch_directory, flags.CLOSE_WRITE) as watcher:
            for event in watcher.next(timeout=2):
                image_file = os.path.join(config.watch_directory, event.name)
                if os.path.exists(image_file):
                    process_image(model, mqtt_client, config, image_file)
    except:
        pass    
    
    mqtt_client.loop_stop()
    mqtt_client.disconnect()

        
        

