import json
import os
import pickle
import sys
from random import *

import cv2
import moviepy.editor as mpy
import mediapipe as mp

from classes.joint import Joint
from classes.pose import Pose


class Utils:

    def __init__(self):
        self.name = "Utils"
        self.jsonfile = "testing.json"
        self.yamlfile = "settings.yaml"
        self.root_dir = os.getcwd()
        self.datafolder = os.sep.join(['data', 'production'])

    def getdict(self):
        """" return the dictionary of all saved data """
        with open(self.jsonfile, "r") as f:
            a = json.load(f)
        return a

    def saveObject(self, object, filename):
        """" saves object to (pickle) file"""
        with open(filename, 'wb') as fp:
            pickle.dump(object, fp)

    def openObject(self, filename):
        """" opens object from (pickle) file"""
        with open(filename, 'rb') as fp:
            object = pickle.load(fp)
        return object

    def embedVideo(self, file):
        cap = cv2.VideoCapture(file)
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()
        allframes = []
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            # Draw the pose annotation on the image.

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            currentframe = []

            for data_point in results.pose_landmarks.landmark:
                # print('x is', data_point.x, 'y is', data_point.y, 'z is', data_point.z,
                #       'visibility is', data_point.visibility)
                currentframe.append(data_point.x)
                currentframe.append(data_point.y)
                currentframe.append(data_point.z)
            allframes.append(currentframe)

            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        cap.release()
        self.saveObject(allframes,"framestest")
        return allframes


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

    def generateJoint(self, name):
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

    def deletefile(self, filename):
        """deletes file from system"""
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print("The file does not exist")

    def ensure_pythonhashseed(self, seed):
        """makes sure to run application with given pythonhashseed so outputs is not random """
        current_seed = os.environ.get("PYTHONHASHSEED")

        seed = str(seed)
        if current_seed is None or current_seed != seed:
            print(f'Setting PYTHONHASHSEED="{seed}"')
            os.environ["PYTHONHASHSEED"] = seed
            # restart the current process
            os.execl(sys.executable, sys.executable, *sys.argv)

    def save_model(self, model, modelname):
        """saves machine learning model"""
        filename = modelname + '.sav'
        pickle.dump(model, open(filename, 'wb'))

    def load_model(self, filename):
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

    def removesound(self, name):
        # TODO: converter maken
        videoclip = mpy.VideoFileClip(name)
        new_clip = videoclip.without_audio()
        new_clip.write_videofile(name.replace("squat0", "no_sound_squat"))

        videoclip.reader.close()
        videoclip.audio.reader.close_proc()
