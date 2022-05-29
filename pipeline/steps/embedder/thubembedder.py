import os

import cv2
import numpy as np
import tensorflow as tf

from pipeline.steps.step import Step


class ThubEmbedder(Step):

    def __init__(self):
        super().__init__()
        self.edges = {
            (0, 1): 'm',
            (0, 2): 'c',
            (1, 3): 'm',
            (2, 4): 'c',
            (0, 5): 'm',
            (0, 6): 'c',
            (5, 7): 'm',
            (7, 9): 'm',
            (6, 8): 'c',
            (8, 10): 'c',
            (5, 6): 'y',
            (5, 11): 'm',
            (6, 12): 'c',
            (11, 12): 'y',
            (11, 13): 'm',
            (13, 15): 'm',
            (12, 14): 'c',
            (14, 16): 'c'
        }
        # squat of 1 video
        self.squat = []
        # laad 'data\\embedders\\thunder_float16.tflite'
        self.embedder = os.sep.join(['data', 'embedders', self.settings['tf_lite_model']])

    def process(self, data) -> list[list[int]]:
        """
        :param data: 1-d List of Strings
        :return: dictionary of 1-d List of Strings (but even spaced so they can be inferred correctly)
            and original queries
        """
        return self.embed(data)

    def embed(self, data: str) -> list[list[int]]:

        print(data)
        #Open een video bestand en maak een Interpreter aan
        cap = cv2.VideoCapture(data)
        interpreter = tf.lite.Interpreter(model_path=self.embedder)
        # interpreter = tf.lite.Interpreter(model_path='thunder.tflite') change 192 to 256
        # interpreter = tf.lite.Interpreter(model_path='thunder_int8.tflite') # unint type echt verschikkelijk traag
        # interpreter = tf.lite.Interpreter(model_path='lightning_int8.tflite') # 192 echt verschikkelijk traag
        # interpreter = tf.lite.Interpreter(model_path='lightning_float16.tflite') goed te doen 192 demensie
        # interpreter = tf.lite.Interpreter(model_path='thunder_float16.tflite') goed te doen 256 demensie
        interpreter.allocate_tensors()

        while cap.isOpened():
            ret, frame = cap.read()

            # Reshape image
            name = self.settings['tf_lite_model']
            resize = 192
            type = tf.float32
            if 'thunder' in name:
                resize = 256
            if 'int8' in name or 'float16' in name:
                type = tf.uint8
            if frame is not None:
                img = frame.copy()

                img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), resize, resize)
                input_image = tf.cast(img, dtype=type)

                # Setup input and output
                input_details = interpreter.get_input_details()
                output_details = interpreter.get_output_details()

                # Make predictions
                interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
                interpreter.invoke()
                keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
                # print(keypoints_with_scores)
                # break

                # Rendering
                # self.draw_connections(frame, keypoints_with_scores, 0.0)
                # self.draw_keypoints(frame, keypoints_with_scores, 0.0)
                self.appendkeypoints(frame, keypoints_with_scores)

                cv2.imshow('MoveNet Lightning', frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        # cap.release()
        # cv2.destroyAllWindows()
        return self.squat

    #Voeg keypoints van poses toe aan list squat
    def appendkeypoints(self, frame, keypoints):
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))
        pose = []

        for index, kp in enumerate(shaped):

            ky, kx, kp_conf = kp
            if index != 16:
                pose.append(ky)
                pose.append(kx)
            elif len(pose) == 32:
                self.squat.append(pose)
                pose = []

    # creëer keypoints van de frames
    def draw_keypoints(self, frame, keypoints, confidence_threshold):
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))

        for kp in shaped:
            ky, kx, kp_conf = kp
            if kp_conf > confidence_threshold:
                cv2.circle(frame, (int(kx), int(ky)), 4, (0, 255, 0), -1)
    
    # Maakt een lineseqment tussen keypoints in het frame
    def draw_connections(self, frame, keypoints, confidence_threshold):
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))

        for edge, color in self.edges.items():
            p1, p2 = edge
            y1, x1, c1 = shaped[p1]
            y2, x2, c2 = shaped[p2]
            if (c1 > confidence_threshold) & (c2 > confidence_threshold):
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
