import json
import os
import pickle
from random import *

from classes.joint import Joint
from classes.pose import Pose


class Utils:

    def __init__(self):
        self.name = "Utils"
        self.jsonfile = "testing.json"
        # self.yamlfile = "settings.yaml"
        self.root_dir = os.getcwd()
        self.datafolder = os.sep.join(['data', 'production'])

    # def getdict(self):
    #     """" return the dictionary of all saved data """
    #     with open(self.jsonfile, "r") as f:
    #         a = json.load(f)
    #     return a
    @staticmethod
    def saveObject(object, filename):
        """" saves object to (pickle) file"""
        with open(filename, 'wb') as fp:
            pickle.dump(object, fp)

    @staticmethod
    def openObject(filename):
        """" opens object from (pickle) file"""
        with open(filename, 'rb') as fp:
            object = pickle.load(fp)
        return object

    # def _checkifexists(self):
    #     """ check if jsonfile exists so that we can do IO operations"""
    #     if not os.path.exists(self.jsonfile):
    #         with open(self.jsonfile, "x") as f:
    #             f.write("{}")
    #
    #     with open(self.jsonfile, "r") as f:
    #         text = f.read()
    #         if len(text) == 0 or text[0] != '{':
    #             with open(self.jsonfile, "w+") as f:
    #                 f.write("{}")
    #
    #     if not os.path.exists(self.yamlfile):
    #         with open(self.yamlfile, "x") as f:
    #             f.write("")

    def generatePose(self):
        """"returns dummy random generated pose"""
        # TODO gezicht weghalen
        sides = ["left", "right"]
        joint_names = ["Eye", "Ear", "Shoulder", "Elbow", "Wrist", "Hip", "Knee", "Ankle"]
        joints = []
        for side in sides:
            for name in joint_names:
                jointname = side + name
                joints.append(self.generateJoint(jointname))
        joints.append(self.generateJoint("nose"))
        return Pose(joints)

    @staticmethod
    def generateJoint(name):
        """"returns dummy random generated Joint"""

        maxInt = 100000
        # TODO randomness vasthouden
        random = Random()
        random.seed(10)
        x = random.randint(0, maxInt + 1)
        y = random.randint(0, maxInt + 1)
        z = random.randint(0, maxInt + 1)
        likelihood = random.randint(0, maxInt + 1)
        joint = Joint(x=x / maxInt * 100, y=y / maxInt * 100, z=z / maxInt * 100, likelihood=likelihood / maxInt,
                      name=name)

        return joint

    def save(self, _dict):
        """saves dictionary to disk"""
        with open(self.jsonfile, "w+") as f:
            json.dump(_dict, f, indent=4)

    @staticmethod
    def deletefile(self, filename):
        """deletes file from system"""
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print("The file does not exist")

    # def ensure_pythonhashseed(self, seed):
    #     """makes sure to run application with given pythonhashseed so outputs is not random """
    #     current_seed = os.environ.get("PYTHONHASHSEED")
    #
    #     seed = str(seed)
    #     if current_seed is None or current_seed != seed:
    #         print(f'Setting PYTHONHASHSEED="{seed}"')
    #         os.environ["PYTHONHASHSEED"] = seed
    #         # restart the current process
    #         os.execl(sys.executable, sys.executable, *sys.argv)

    @staticmethod
    def save_model(model, modelname):
        """saves machine learning model"""
        filename = modelname + '.sav'
        pickle.dump(model, open(filename, 'wb'))

    @staticmethod
    def load_model(filename):
        """loads given machine loading model"""
        filename += ".sav"
        loaded_model = pickle.load(open(filename, 'rb'))
        return loaded_model

    # def load_yaml(self):
    #     """laods yamlfile """
    #     """returns settings type of dictionary"""
    #     with open(self.yamlfile, "r") as f:
    #         data = yaml.load(f, Loader=yaml.FullLoader)
    #     return data

    #
    # def save_yaml(self, data):
    #     """saves data to a yaml file"""
    #     with open(self.yamlfile, "w") as f:
    #         yaml.dump_all(data, f)
    # propably not needed ^^

    # def load_settings(self):
    #     """loads yamlfile """
    #     """returns settings type of dictionary"""
    #     with open(self.yamlfile, "r") as f:
    #         data = yaml.load(f, Loader=yaml.FullLoader)
    #     return data["settings"]
