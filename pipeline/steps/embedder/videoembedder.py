import os

import cv2
import mediapipe as mp

from pipeline.steps.embedder.embedder import Embedder
from pipeline.utils.utils import Utils

from typing import Set


"""
Embedder class
used to embed video material
"""


class VideoEmbeder(Embedder):

    def process(self, data)-> None:
        """
        :param data: 1-d List of Strings
        :return: dictionary of 1-d List of Strings (but even spaced so they can be inferred correctly)
            and original queries
        """
        points = self._embedVideo(data)

        return points

    def _embedVideo(self, video)"""-> Set[sizeOf(results.pose_landmarks.landmark)]""": # dit moet nog worden bijgewerkt
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

                for data_point in results.pose_landmarks.landmark:
                    # print('x is', data_point.x, 'y is', data_point.y, 'z is', data_point.z,
                    #       'visibility is', data_point.visibility)
                    normalized = False
                    if normalized:
                        currentframe.append(data_point.x)
                        currentframe.append(data_point.y)
                        currentframe.append(data_point.z)
                    else:
                        currentframe.append(data_point.x * width)
                        currentframe.append(data_point.y * height)
                        currentframe.append(data_point.z)

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
