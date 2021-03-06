import os

import cv2
import mediapipe as mp
import numpy as np

from pipeline.steps.embedder.videoembedder import Embedder
from pipeline.utils.utils import Utils

"""
Embedder class
used to embed video material
"""

landmarks_config = {
    0: "nose",
    1: "left_eye_inner",
    2: "left_eye",
    3: "left_eye_outer",
    4: "right_eye_inner",
    5: "right_eye",
    6: "right_eye_outer",
    7: "left_ear",
    8: "right_ear",
    9: "mouth_left",
    10: "mouth_right",
    11: "left_shoulder",
    12: "right_shoulder",
    13: "left_elbow",
    14: "right_elbow",
    15: "left_wrist",
    16: "right_wrist",
    17: "left_pinky",
    18: "right_pinky",
    19: "left_index",
    20: "right_index",
    21: "left_thumb",
    22: "right_thumb",
    23: "left_hip",
    24: "right_hip",
    25: "left_knee",
    26: "right_knee",
    27: "left_ankle",
    28: "right_ankle",
    29: "left_heel",
    30: "right_heel",
    31: "left_foot_index",
    32: "right_foot_index",
}


class MPEmbedder(Embedder):
    """ Embed a video file using MediaPipe """

    def process(self, data: None) -> None:
        """ Processes the data """
        data = os.listdir(os.sep.join(["data", "positive_squat"]))
        data += os.listdir(os.sep.join(["data", "negative_squat"]))
        testdata = os.listdir(os.sep.join(["data", "production"]))

        if self.settings["trainmode"]:
            for file in data:
                print(file)
                self.embed(file)

        if not self.settings["trainmode"]:
            for file in testdata:
                self.embed_test_squat(file)

    def embed(self, data: str) -> None:
        """ Embeds the data """
        folder = 'production'
        if 'positive' in data:
            folder = 'positive_squat'
        elif 'negative' in data:
            folder = 'negative_squat'
        video_title = data.split('.')[0]
        # haalt de default waarde van de landmarks op
        video_location = os.sep.join(["data", folder, data])

        embedded_location = os.sep.join(["data", "embedded", video_title])
        if folder == 'production':
            embedded_location = os.sep.join(["data", "embedded_test", video_title])
        if os.path.exists(embedded_location):
            return
        print(f"embedding: {data}")
        cap = cv2.VideoCapture(video_location)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print("width: ", width)
        print("height: ", height)
        # mp_drawing = mp.solutions.drawing_utils
        # mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(model_complexity=2)

        allframes = []
        all_flipped_frames = []
        percentage = 0
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            # Om de prestaties te verbeteren, is de afbeelding gemarkeerd als niet beschrijfbaar
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            # # Teken de pose annotation op de afbeelding.
            # image.flags.writeable = True
            # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            currentframe = []
            current_flipped_frame = []

            if results.pose_landmarks is None:
                print("No pose results.")
                # currentframe.append(image)
            else:
                for index, data_point in enumerate(results.pose_landmarks.landmark):
                    # print('x is', data_point.x, 'y is', data_point.y, 'z is', data_point.z,
                    #       'visibility is', data_point.visibility)

                    if landmarks_config[index] in self.settings["landmarks_to_pick"]:

                        # Als settings staat op 'normalize_landmarks' voeg de data points to aan de list
                        # "currentframe" Voor alle andere settings worden de data punten eerste aangepast en daarna
                        # toegevoegd aan de list "currentframe"
                        # print(landmarks_config[index], ": ", data_point.x, data_point.y, data_point.z)

                        currentframe.append(data_point.x)
                        currentframe.append(data_point.y)
                        currentframe.append(data_point.z)
                        if folder != "production":
                            current_flipped_frame.append(1 - data_point.x)
                            current_flipped_frame.append(1 - data_point.x)
                            current_flipped_frame.append(data_point.z)

                        percentage += 1
                        # print(index, data_point.x * width, data_point.y * height)
            print('{:.2f} %'.format(round(percentage / frame_count * 10, 2)))
            allframes.append(currentframe)
            if folder != "production":
                all_flipped_frames.append(current_flipped_frame)

            # mp_drawing.draw_landmarks(
            #     image,
            #     results.pose_landmarks,
            #     mp_pose.POSE_CONNECTIONS,
            #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        cap.release()
        squat = np.array(allframes)
        flipped_squat = np.array(all_flipped_frames)
        Utils().saveObject(squat, embedded_location)
        print(f"this is folder {folder}")
        if folder != 'production':
            Utils().saveObject(flipped_squat, embedded_location + '_flipped')
        return

    def scalevalue(self, val, minmaxvalues):
        # Give the appropriate dimension in the values
        returntuple = (val - minmaxvalues['min']) / (minmaxvalues['max'] - minmaxvalues['min'])
        return returntuple

    def scalesquat(self, squat):
        minmaxvalues = self.minmaxvals(squat)
        iterator = 1
        for i, frame in enumerate(squat):
            for j, coordinate in enumerate(frame):
                if iterator % 3 == 1:
                    squat[i][j] = self.scalevalue(coordinate, minmaxvalues[0])
                elif iterator % 3 == 2:
                    squat[i][j] = self.scalevalue(coordinate, minmaxvalues[1])
                elif iterator % 3 == 0:
                    squat[i][j] = self.scalevalue(coordinate, minmaxvalues[2])
                iterator += 1
            iterator = 1
        return squat

    def minmaxvals(self, squat):
        iterator = 1
        # current = ''
        xVals = {'min': None, 'max': None}
        yVals = {'min': None, 'max': None}
        zVals = {'min': None, 'max': None}

        def setvals(vals, value):
            if vals['min'] is None or vals['min'] > value:
                vals['min'] = value
            if vals['max'] is None or vals['max'] < value:
                vals['max'] = value
            return vals

        for frame in squat:
            for coordinate in frame:
                if iterator % 3 == 1:
                    # current = 'x'
                    xVals = setvals(xVals, coordinate)
                elif iterator % 3 == 2:
                    yVals = setvals(yVals, coordinate)
                    # current = 'y'
                elif iterator % 3 == 0:
                    zVals = setvals(zVals, coordinate)
                    # current = 'z'
                iterator += 1
            iterator = 1
        return xVals, yVals, zVals

    def embed_test_squat(self, data: str) -> None:
        """ Embeds production data """
        folder = 'production'
        video_title = data.split('.')[0]
        # haalt de default waarde van de landmarks op
        video_location = os.sep.join(["data", folder, data])
        embedded_location = os.sep.join(["data", "embedded_test", video_title])
        if os.path.exists(embedded_location):
            return Utils.openEmbedding(video_title, "embedded_test")
        print(f"embedding: {data}")
        cap = cv2.VideoCapture(video_location)
        print(f"video_location: {video_location}")
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print("width: ", width)
        print("height: ", height)
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(model_complexity=2)

        allframes = []
        percentage = 0
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            # Om de prestaties te verbeteren, is de afbeelding gemarkeerd als niet beschrijfbaar
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            # # Teken de pose annotation op de afbeelding.
            # image.flags.writeable = True
            # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            currentframe = []
            current_flipped_frame = []

            if results.pose_landmarks is None:
                print("No pose results.")
                # currentframe.append(image)
            else:
                for index, data_point in enumerate(results.pose_landmarks.landmark):
                    # print('x is', data_point.x, 'y is', data_point.y, 'z is', data_point.z,
                    #       'visibility is', data_point.visibility)

                    if landmarks_config[index] in self.settings["landmarks_to_pick"]:
                        # Als settings staat op 'normalize_landmarks' voeg de data points to aan de list
                        # "currentframe" Voor alle andere settings worden de data punten eerste aangepast en daarna
                        # toegevoegd aan de list "currentframe"
                        # print(landmarks_config[index], ": ", data_point.x, data_point.y, data_point.z)

                        currentframe.append(data_point.x)
                        currentframe.append(data_point.y)
                        currentframe.append(data_point.z)

                        percentage += 1
                        # print(index, data_point.x * width, data_point.y * height)
            print('{:.2f} %'.format(round(percentage / frame_count * 10, 2)))
            allframes.append(currentframe)

            # mp_drawing.draw_landmarks(
            #     image,
            #     results.pose_landmarks,
            #     mp_pose.POSE_CONNECTIONS,
            #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        cap.release()
        squat = np.array(allframes)
        Utils().saveObject(squat, embedded_location)
        print(f"this is folder {folder}")
        newSquat = self.scalesquat(squat)
        return newSquat
