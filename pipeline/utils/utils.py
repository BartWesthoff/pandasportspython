import copy
import itertools
import json
import os
import pickle
import sys
from random import *

import numpy as np
import yaml
from keras import Sequential
from keras.applications.densenet import layers
from keras.layers import Dense


from classes import joint
from classes import pose
from pipeline.utils.deprecated import deprecated
from pipeline.models.model import Model

class Utils:

    def __init__(self) -> None:
        self.name = "Utils"
        self.jsonfile = "testing.json"
        self.root_dir = os.getcwd()
        self.datafolder = os.sep.join(['data', 'production'])

    @deprecated
    def getdict(self):
        """" return the dictionary of all saved data """
        with open(self.jsonfile, "r") as f:
            a = json.load(f)
        return a

    @staticmethod
    def saveObject(obj: object, filename: str) -> None:  # wat is object
        """" saves object to (pickle) file"""
        with open(filename, 'wb') as fp:
            print(f"saving object {filename}")
            pickle.dump(obj, fp)

    @staticmethod
    def saveSquatEmbedding(squats: list[list[int]], filename: str) -> None:  # wat is object
        """" saves object to (pickle) file"""
        save_location = os.sep.join(["data", "embedded", filename])
        print(save_location)
        with open(save_location, 'wb') as fp:
            print(f"saving object {filename}")
            pickle.dump(squats, fp)



    @staticmethod
    def saveModel(model: Model) -> None:  # wat is object
        """" saves object to (pickle) file"""
        with open(model.name, 'wb') as fp:
            print(f"saving object {model.name}")
            pickle.dump(model, fp)

    @staticmethod
    def openObject(filename: str) -> object:
        """" returns object from (pickle) file"""
        with open(filename, 'rb') as inputfile:
            obj = pickle.load(inputfile)
        return obj

    @staticmethod
    def openEmbedding(filename: str) -> np.ndarray:
        """"returns object from (pickle) file"""
        with open(os.sep.join(["data", "embedded", filename]), 'rb') as inputfile:
            obj = pickle.load(inputfile)
        return obj

    # @staticmethod
    # def openObject(filename: str) -> np.ndarray | abc.Iterable | int | float:  # return object
    #    """" opens object from (pickle) file"""
    #    with open(filename, 'rb') as fp:
    #        object = pickle.load(fp)
    #    return object

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

    def generatePose(self) -> pose.Pose:
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
        return pose.Pose(joints)

    @staticmethod
    def generateJoint(name: str) -> joint.Joint:  # wat is joint
        """"returns dummy random generated Joint"""

        maxInt = 100000
        random = Random()
        x = random.randint(0, maxInt + 1)
        y = random.randint(0, maxInt + 1)
        z = random.randint(0, maxInt + 1)
        likelihood = random.randint(0, maxInt + 1)
        join = joint.Joint(x=x / maxInt * 100, y=y / maxInt * 100, z=z / maxInt * 100, likelihood=likelihood / maxInt,
                           name=name)
        return join

    def generatePoseList(self, frames: int, poses: int) -> list[list[int]]:
        """"generates a random list of poses that are a squat"""
        random = Random()
        squat = []
        for _ in range(frames):
            pose = []
            for i in range(poses * 3):
                x = random.randint(0, 1080)
                y = random.randint(0, 1920)
                z = random.randint(0, 100)

                pose.append(x)
                pose.append(y)
                pose.append(z)
            squat.append(pose)
        return squat

    def save(self, _dict: dict) -> None:
        """saves dictionary to disk"""
        with open(self.jsonfile, "w+") as f:
            json.dump(_dict, f, indent=4)

    @staticmethod
    def deletefile(filename: str) -> None:
        """deletes file from system"""
        if os.path.exists(filename):
            os.remove(filename)
        else:
            raise FileNotFoundError("The file does not exist")

    @deprecated
    def ensure_pythonhashseed(self, seed):
        """makes sure to run application with given pythonhashseed so outputs is not random """
        current_seed = os.environ.get("PYTHONHASHSEED")

        seed = str(seed)
        if current_seed is None or current_seed != seed:
            print(f'Setting PYTHONHASHSEED="{seed}"')
            os.environ["PYTHONHASHSEED"] = seed
            # restart the current process
            os.execl(sys.executable, sys.executable, *sys.argv)

    @staticmethod
    def save_model(model: object, modelname: str) -> None:
        """saves machine learning model"""

        # TODO: folder veranderen
        filename = modelname + '.sav'
        pickle.dump(model, open(filename, 'wb'))

    @staticmethod
    def load_model(filename: str):  # return type model inzien, is een list of set
        """loads given machine loading model"""
        filename += ".sav"
        # TODO: folder veranderen
        loaded_model = pickle.load(open(filename, 'rb'))
        return loaded_model

    @deprecated
    def load_yaml(self):
        """laods yamlfile """
        """returns settings type of dictionary"""
        with open(self.yamlfile, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data

    @deprecated
    def save_yaml(self, data):
        """saves data to a yaml file"""
        with open(self.yamlfile, "w") as f:
            yaml.dump_all(data, f)

    @staticmethod
    def load_settings() -> dict:
        """loads yamlfile and returns settings type of dictionary"""
        with open("settings.yaml", "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data["settings"]

    @staticmethod
    def augmentation(squat: list, spread: int) -> list[list[int]]:
        """augmentation of the squats to make more squats"""
        # TODO: random spread toevoegen
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
    def changeFileName(filename: str, newname: str) -> str:
        """changes the filename of a file"""
        path = os.sep.join(filename.split(os.sep)[:-1])
        output_source = os.sep.join([path, newname])
        return output_source

    @staticmethod
    def define_model() -> Sequential:
        """defines sequential model"""
        # input1 = Input(shape=(137, 99, 1))  # take the reshape last two values, see "data = np.reshape(data,(137,
        # 99,1))" which is "data/batch-size, row, column"
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

    # Functie om met de training data te spelen
    def playground(self):
        """"playground function. Meant for saving dummy code for testing or demonstrating"""
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
