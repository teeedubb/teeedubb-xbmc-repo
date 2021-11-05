import os.path
import re


class raspberry:

    def __init__(self):
        self.model_path = '/proc/device-tree/model'
        self.pattern = 'raspberry pi'

    def is_raspberry_pi(self):
        if not os.path.isfile(self.model_path):
            return False
        with open(self.model_path, 'r') as model:
            for line in model:
                if re.search(self.pattern, line, re.IGNORECASE):
                    return True
        return False
