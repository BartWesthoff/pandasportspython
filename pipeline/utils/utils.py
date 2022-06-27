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
from numpy import ndarray

from classes import joint
from classes import pose
from pipeline.utils.deprecated import deprecated


class Utils:

    def __init__(self) -> None:
        """initializes the Utils class"""
        self.name = "Utils"
        self.jsonfile = "testing.json"
        self.root_dir = os.getcwd()
        self.yamlfile = "settings.yaml"
        self.datafolder = os.sep.join(["data", "production"])

    @deprecated
    def getdict(self):
        """" return the dictionary of all saved data """
        with open(self.jsonfile, "r") as f:
            a = json.load(f)
        return a

    @staticmethod
    def saveObject(obj: object, filename: str) -> None:  # wat is object
        """" saves object to (pickle) file"""
        with open(filename, "wb") as fp:
            print(f"saving object {filename}")
            pickle.dump(obj, fp)

    @staticmethod
    def saveSquatEmbedding(squat: ndarray, filename: str) -> None:  # wat is object
        """" saves object to (pickle) file"""
        save_location = os.sep.join(["data", "embedded", filename])
        print(save_location)

        if os.path.exists(save_location):
            print(f"{save_location} already exists")
            return
        with open(save_location, "wb") as fp:
            print(f"saving object {filename}")
            pickle.dump(squat, fp)

    @staticmethod
    def saveModel(model) -> None:  # wat is object
        """" saves object to (pickle) file"""
        with open(model.__str__(), "wb") as fp:
            print(f"saving object {model.__str__()}")
            pickle.dump(model, fp)

    @staticmethod
    def openObject(filename: str) -> object:
        """" returns object from (pickle) file"""
        with open(filename, "rb") as inputfile:
            obj = pickle.load(inputfile)
        return obj

    @staticmethod
    def openEmbedding(filename: str) -> np.ndarray:
        """"returns object from (pickle) file"""
        with open(os.sep.join(["data", "embedded", filename]), "rb") as inputfile:
            obj = pickle.load(inputfile)
        return obj

    @staticmethod
    def openTestEmbedding(filename: str) -> np.ndarray:
        """"returns object from (pickle) file"""
        with open(os.sep.join(["data", "testdata", filename]), "rb") as inputfile:
            obj = pickle.load(inputfile)
        return obj

    # @staticmethod
    # def openObject(filename: str) -> np.ndarray | abc.Iterable | int | float:  # return object
    #    """" opens object from (pickle) file"""
    #    with open(filename, "rb") as fp:
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
    #         if len(text) == 0 or text[0] != "{":
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
            print(f"Setting PYTHONHASHSEED={seed}")
            os.environ["PYTHONHASHSEED"] = seed
            # restart the current process
            os.execl(sys.executable, sys.executable, *sys.argv)

    @staticmethod
    def save_model(model: object, modelname: str) -> None:
        """saves machine learning model"""

        # TODO: folder veranderen
        filename = modelname + ".sav"
        pickle.dump(model, open(filename, "wb"))

    @staticmethod
    def load_model(filename: str):  # return type model inzien, is een list of set
        """loads given machine loading model"""
        filename += ".sav"
        # TODO: folder veranderen
        loaded_model = pickle.load(open(filename, "rb"))
        return loaded_model

    @deprecated
    def load_yaml(self):
        """laods yamlfile """
        """returns settings type of dictionary"""
        with open(self.yamlfile, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data

    def save_yaml(self, data):
        """saves data to a yaml file"""
        with open(self.yamlfile, "w") as f:
            yaml.dump(data, f)

    def load_settings(self) -> dict:
        """loads yamlfile and returns settings type of dictionary"""
        with open(self.yamlfile, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data["settings"]

    def augmentation(self, name: str, squat: ndarray, spreadx: int = None, spready: int = None, width: int = None,
                     height: int = None, amount: int = 10, save: bool = False) -> ndarray:
        """augmentation of the squats to make more squats"""
        # TODO: random spread toevoegen
        if self.load_settings()["normalize_landmarks"] and (spreadx is None or spready is None):
            raise ValueError("spreadx and spready must be given if normalize_landmarks is True")
        if spreadx is None:
            spreadx = randint(10, 100)
        if spready is None:
            spready = randint(10, 100)
        random_x = [i for i in range(-spreadx // 2, spreadx // 2 + 1, 5) if i != 0]
        random_y = [i for i in range(-spready // 2, spready // 2 + 1, 5) if i != 0]
        c = list(itertools.product(random_x, random_y))
        squats = []
        for combination in c:
            new_squat = []
            for frame in squat:
                lenght = len(frame)
                modified_array = copy.deepcopy(frame)
                for i in range(0, lenght, 3):
                    modified_array[i] += combination[0] / 1 if width is None else combination[0] / width
                    modified_array[i + 1] += combination[1] / 1 if height is None else combination[0] / height
                new_squat.append(modified_array)
            squats.append(new_squat)
        shuffle(squats)
        random_squats = np.array(squats)[:amount]
        if save:
            for idx, i in enumerate(random_squats):
                Utils().saveSquatEmbedding(i, f"{name}_augmented{idx + 1}")
        return random_squats

    @staticmethod
    def changeFileName(filename: str, newname: str) -> str:
        """changes the filename of a file"""
        path = os.sep.join(filename.split(os.sep)[:-1])
        if '.mp4' not in newname:
            newname += '.mp4'
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
        model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
        # model.summary()
        return model

    def data_augmentation_normalized(self, name: str, squat: ndarray, spreadx: int = None, spready: int = None,
                                     amount: int = 10, save: bool = False) -> ndarray:
        """augmentation of the squats to make more squats (normalized)"""
        low_x = 1
        low_y = 1
        high_x = 0
        high_y = 0
        for frame in squat:
            lenght = len(frame)
            for i in range(0, lenght, 3):
                ## kijkt steeds of hoogste y (bijv 0.76 lager is dan 1 of vorige waarde)
                ## kijkt steeds of hoogste x (bijv 0.80 lager is dan 1 of vorige waarde)

                low_x = frame[i] if frame[i] < low_x else low_x
                low_y = frame[i + 1] if frame[i + 1] < low_y else low_y
                high_x = frame[i] if frame[i] > high_x else high_x
                high_y = frame[i + 1] if frame[i + 1] > high_y else high_y

        # om getatl tussen de 0 en 100 te krijgen voor de randint
        low_x = low_x * 100
        low_y = low_y * 100
        high_x = high_x * 100
        high_y = high_y * 100
        spready = randint(int(low_y), int(high_y)) if spready is None else spready
        spreadx = randint(int(low_x), int(high_x)) if spreadx is None else spreadx

        # hier weer omzetten naar %
        random_x = [i // 100 for i in range(-spreadx // 2, spreadx // 2 + 1) if i != 0]
        random_y = [i // 100 for i in range(-spready // 2, spready // 2 + 1) if i != 0]
        c = list(itertools.product(random_x, random_y))
        shuffle(c)

        squats = []

        for combination in c[:amount]:
            new_squat = []
            for frame in squat:
                lenght = len(frame)
                modified_array = copy.deepcopy(frame)
                for i in range(0, lenght, 3):
                    modified_array[i] += combination[0]
                    modified_array[i + 1] += combination[1]

                new_squat.append(modified_array)
            squats.append(new_squat)

        random_squats = np.array(squats)
        if save:
            for idx, squat in enumerate(random_squats):
                Utils().saveSquatEmbedding(squat, f"{name}_augmented{idx + 1}")
        return random_squats

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

    def check_invalid_squats(self):
        checked = []
        for current in list(os.listdir(os.sep.join(["data", "embedded"]))):

            # # if np.array_equal(current_squat, example_squat):
            # #     print(f"{current} and {example} are the same")
            # #     os.remove(os.sep.join(["data", "embedded", current]))
            # #     break
            # # if example_squat.shape[1] != 30:
            # #     print(f"{example} has wrong shape")
            # #     os.remove(os.sep.join(["data", "embedded", example]))
            # #     break
            # if os.path.exists(os.sep.join(["data", "embedded", current])):
            squat = self.openEmbedding(current)
            for frame in squat:
                for idx, coordinaat in enumerate(frame):
                    if (coordinaat < 0 or coordinaat > 1) and (idx + 1) % 3 != 0:
                        if os.path.exists(os.sep.join(["data", "embedded", current])):
                            os.remove(os.sep.join(["data", "embedded", current]))
                            print(f"{current} is invalid")
                            break
