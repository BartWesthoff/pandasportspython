from pipeline.steps.embedder.embedder import Embedder
import cv2
import mediapipe as mp
"""
Embedder class
used to embed video material
"""

# Goal of this step is to capture & display the data points onto the current frame
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
        # Initialiseer mediapipe video
        cap = cv2.VideoCapture(video)
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        # mediapipepose
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()
        allframes = []
        while cap.isOpened():
            # grabs & decodes the frame
            success, image = cap.read()
            if not success:
                break

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # gets pose
            results = pose.process(image)

            # Draw the pose annotation on the image.

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            currentframe = []

            # cycle through all datapoints, add to current frame
            for data_point in results.pose_landmarks.landmark:
                # print('x is', data_point.x, 'y is', data_point.y, 'z is', data_point.z,
                #       'visibility is', data_point.visibility)
                currentframe.append(data_point.x)
                currentframe.append(data_point.y)
                currentframe.append(data_point.z)
            #add new frame  
            allframes.append(currentframe)
            
            # add everything to current frame
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        cap.release()
        self.saveObject(allframes, "framestest")
        return allframes

