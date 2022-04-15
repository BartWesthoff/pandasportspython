from pipeline.steps.embedder.embedder import Embedder
import cv2
import mediapipe as mp
from pipeline.utils.utils import Utils
"""
Embedder class
used to embed video material
"""


class VideoEmbeder(Embedder):

    def process(self, data):
        """
        :param data: 1-d List of Strings
        :return: dictionary of 1-d List of Strings (but even spaced so they can be inferred correctly)
            and original queries
        """
        self._embedVideo(data)

        return

    def _embedVideo(self, video):
        """
        :param query: string
        :return: modified string
        """
        #haalt de default waarde van de landmarks op
        cap = cv2.VideoCapture(video)
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
            #Maakt list met floats van de poselandmarks
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
        Utils().saveObject(allframes, "framestest")
        return allframes

