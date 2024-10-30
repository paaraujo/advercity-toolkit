
import yaml
import os
from PIL import Image


def list_folders(directory):
    ''' Get all folders inside a directory.
    '''
    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    return folders


class AdverCityDataset:

    def __init__(self, root='', car=0, cam=0):
        # Check if root is a valid path
        if not os.path.exists(root):
            raise Exception("'root' is not a valid path.") 

        self._root = root
        self._car  = car
        self._cam = cam

        # Getting all agents available in the scenario
        self._agents = sorted([folder for folder in list_folders(self._root)])
        self._rsus = self._agents[:-2]
        self._cars = self._agents[2:]
        
        # Getting all timestamps
        self._timestamps = sorted([f.split('.')[0] for f in os.listdir(os.path.join(self._root, self._cars[self._car])) if f.endswith(('.yaml', '.yml')) and not 'gnss' in f])
        
    def __len__(self):
        return len(self._timestamps)

    def __getitem__(self, index):
        # Getting camera reference position
        with open(os.path.join(self._root, self._cars[self._car], self._timestamps[index]+'.yaml'), 'r') as file:
            data = yaml.safe_load(file)
        car_speed = data.get('ego_speed')
        cam_ref = data.get('camera'+str(self._cam), {}).get('cords')
        cam_ref = [cam_ref[0], cam_ref[1], cam_ref[2], cam_ref[3], cam_ref[5], cam_ref[4], car_speed]
        cam_intrinsics = data.get('camera'+str(self._cam), {}).get('intrinsic')
        cam_image = Image.open(os.path.join(self._root, self._cars[self._car], self._timestamps[index] + '_camera' + str(self._car) + '.png'))
        return (cam_ref, cam_intrinsics, cam_image)
