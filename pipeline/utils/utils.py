import copy
import itertools
import json
import os
import pickle
from random import *

import numpy as np
import yaml
from keras import Sequential
from keras.applications.densenet import layers
from keras.layers import Dense

from classes.joint import Joint
from classes.pose import Pose

# Type hinting
from typing import List


class Utils:

    def __init__(self) -> None:
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
    def saveObject(object, filename: str) -> None: # wat is object
        """" saves object to (pickle) file"""
        with open(filename, 'wb') as fp:
            print("saving object")
            pickle.dump(object, fp)

    @staticmethod
    def openObject(filename: str): # return object
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
 
     def generatePose(self) -> List(str, str, str, str, str, str, str, str):
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
    def generateJoint(name: str): # wat is joint
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

    def save(self, _dict) -> None:
        """saves dictionary to disk"""
        with open(self.jsonfile, "w+") as f:
            json.dump(_dict, f, indent=4)

    @staticmethod
    def deletefile(filename):
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
    def save_model(model, modelname) -> None: 
        """saves machine learning model"""
        filename = modelname + '.sav'
        pickle.dump(model, open(filename, 'wb'))

    @staticmethod
    def load_model(filename): # return type model inzien, is een list of set
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
    @staticmethod
    def load_settings():
        """loads yamlfile """
        """returns settings type of dictionary"""
        with open("settings.yaml", "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data["settings"]

    @staticmethod
    def augmentation(squat: list, spread: int):
        random_x = [i for i in range(-spread // 2, spread // 2 + 1) if i != 0]
        random_y = [i for i in range(-spread // 2, spread // 2 + 1) if i != 0]
        c = list(itertools.product(random_x, random_y))
        squats = []

        for combination in c:
            new_squat = []
            for frame in squat:
                lenght = len(frame)
                modified_array = copy.deepcopy(frame)
                for i in range(0, lenght, 3):
                    modified_array[i] += combination[0]
                    modified_array[i + 1] += combination[1]
                new_squat.append(modified_array)
            squats.append(new_squat)
        return squats

    @staticmethod
    def changeFileName(fileName, newName):
        path = os.sep.join(fileName.split(os.sep)[:-1])
        output_source = os.sep.join([path, newName])
        return output_source

    @staticmethod
    def define_model():
        # input1 = Input(shape=(137, 99,
        #                       1))  # take the reshape last two values, see "data = np.reshape(data,(137,99,1))" which is "data/batch-size, row, column"
        #
        # dnn_output = Dense(1)

        model = Sequential()
        # Add an Embedding layer expecting input vocab of size 1000, and
        # output embedding dimension of size 64.
        # model.add(Embedding(input_dim=1, output_dim=64))

        # Add a LSTM layer with 128 internal units.
        model.add(layers.LSTM(128, input_shape=(137, 99)))

        # Add a Dense layer with 10 units.
        model.add(Dense(64, activation="relu"))
        model.add(Dense(1, activation="sigmoid"))
        # compile the model
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        # model.summary()
        return model

    def playground(self):
        # define model for simple BI-LSTM + DNN based binary classifier

        train_data = Utils().openObject("400 squats")
        # print(allframes)
        data = np.array(train_data)  # (137,99) (frames, joints*3)

        Y = [1 for _ in range(0, 400)]  # Class label for the dummy data
        print("data = ", data)
        # Reshape the data into 3-D numpy array
        data = np.reshape(data, (400, 137, 99))  # Here we have a total of 10 rows or records
        print("data after reshape => ", data)
        # Call the model
        model = self.define_model()
        # fit the model
        model.fit(data, np.array(Y), epochs=2, batch_size=2, verbose=1)

        # Take a test data to test the working of the model
        correct_pose = Utils().openObject("voorbeeld")
        test_data = np.array(correct_pose)
        # reshape the test data
        test_data = np.reshape(test_data, (1, 137, 99))
        pred = model.predict(test_data)
        print("predicted sigmoid output => ", pred)
