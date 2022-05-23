import os

import cv2
import mediapipe as mp

from pipeline.steps.step import Step
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

# landmarks_config  but the values are the keys
# misschien niet nodig
landmarks_config_reverse = {
    "nose": 0,
    "left_eye_inner": 1,
    "left_eye": 2,
    "left_eye_outer": 3,
    "right_eye_inner": 4,
    "right_eye": 5,
    "right_eye_outer": 6,
    "left_ear": 7,
    "right_ear": 8,
    "mouth_left": 9,
    "mouth_right": 10,
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_pinky": 17,
    "right_pinky": 18,
    "left_index": 19,
    "right_index": 20,
    "left_thumb": 21,
    "right_thumb": 22,
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
    "left_heel": 29,
    "right_heel": 30,
    "left_foot_index": 31,
    "right_foot_index": 32,
}


class VideoEmbeder(Step):

    def process(self, data) -> list[list[float]]:
        """
        :param data: 1-d List of Strings
        :return: dictionary of 1-d List of Strings (but even spaced so they can be inferred correctly)
            and original queries
        """
        points = self._embedVideo(data)
        return points

    def _embedVideo(self, video: str) -> list[list[float]]:
        # -> Set[sizeOf(results.pose_landmarks.landmark)]
        # dit moet nog worden bijgewerkt
        """
        :param query: string
        :return: modified string
        """
        cap = cv2.VideoCapture(video)
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()

        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
        print("width: ", width)
        print("height: ", height)
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
            if results.pose_landmarks is None:
                print("No pose results.")
                # currentframe.append(image)
            else:
                for index, data_point in enumerate(results.pose_landmarks.landmark):
                    # print('x is', data_point.x, 'y is', data_point.y, 'z is', data_point.z,
                    #       'visibility is', data_point.visibility)
                    if landmarks_config[index] in self.settings["landmarks_to_pick"]:

                        print(landmarks_config[index], ": ", data_point.x, data_point.y, data_point.z)
                        normalized = False
                        if normalized:
                            currentframe.append(data_point.x)
                            currentframe.append(data_point.y)
                            currentframe.append(data_point.z)
                        else:
                            currentframe.append(data_point.x * width)
                            currentframe.append(data_point.y * height)
                            currentframe.append(data_point.z)
                        # print(index, data_point.x * width, data_point.y * height)

            allframes.append(currentframe)

            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        cap.release()
        name = "voorbeeld"
        if os.path.isfile(name):
            frames = Utils.openObject(name)
            frames.append(allframes)
            Utils.saveObject(frames, name)
        else:
            Utils().saveObject([allframes], name)

        return allframes
