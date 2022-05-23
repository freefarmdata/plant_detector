from dataclasses import dataclass, asdict, field
import json
import os

@dataclass
class Model:

    lower_color: list = field(default_factory=lambda: [55, 70, 70])
    upper_color: list = field(default_factory=lambda: [80, 255, 255])
    blur_kernel: list = field(default_factory=lambda: [5, 5])
    dilate_kernel: list = field(default_factory=lambda: [5, 5])
    denoise_temp_size: int = 50
    denoise_window_size: int = 50
    denoise_strength: int = 20
    bbox_min_area: int = 3000

    def load(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                parameters = json.load(f)
                for parameter in parameters.keys():
                    setattr(self, parameter, parameters[parameter])
    
    def save(self, file_path):
        with open(file_path, 'w') as f:
            json.dump(asdict(self), f)