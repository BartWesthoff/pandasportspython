import os
import time
from random import *

import numpy as np
from sklearn import svm
from sklearn.svm import SVC

from pipeline.steps.embedder.thubembedder import ThubEmbedder
from pipeline.steps.input.input import GoogleDriveService
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.steps.training.videotraining import VideoTrainer
from pipeline.utils.utils import Utils
from timeit import default_timer as timer
from datetime import timedelta
import keyboard  # using module keyboard

if __name__ == "__main__":

    #VideoTrainer().process('')
    # clf = Utils.openObject('SVMmodel')
    # for i in range(0, 100):
    #     array = np.array(Utils().generatePoseList(10, 10)).reshape(1, 900)
    #     print(clf.predict(array)[0], end=" ")
    #

    #importeert bestand van de Google drive en slaat het op onder de aangegeven naam
    #squat = ThubEmbedder().process(os.sep.join([Utils().datafolder, '20220330_121948_Trim5.mp4']))
    ## squat to numpy array
    #array = np.array(squat)
    #Utils().saveObject(array, 'squatTFHUB')


    #Opent de file en slaat het op als een N-dimensional array
    squat = Utils().openObject('squatTFHUB')
    print(squat.shape)
    #Code om de N-dimensional array om te zetten naar een contiguous flattened array(1D array)
    squat2 = squat.ravel()
    print(squat2.shape)
    #Importeert SVC model en fit de squat
    model = SVC()
    model.fit([squat2,squat2], [0,1])
    answer = model.predict([squat2])
    print(answer)

    test =ThubEmbedder()

    print("dada")

    #laat een scatter plot zien van de accuratesse
    import matplotlib.pyplot as plt 

    plt.title('SVC vs accuracy')
    plt.scatter(answer, answer, label='Testing Accuracy')
    plt.legend()
    plt.xlabel('Number of squads')
    plt.ylabel('Accuracy')

    plt.show()

    

    # source = os.sep.join(['data', 'production', '20220330_111746_Trim1.mp4'])
    # VideoPreProcessor().playVideo(source)


    video = "20220524_131227"
    output = "videoshort"
    VideoPreProcessor().crop(source=video, end=49.00, start=20.13, output=output)

    # while True:
    #
    #     if 0xFF == ord('q'):

    # start = timer()
    #
    # end = timer()
    # delta = timedelta(seconds=end - start)
    # print(str(delta)[:-3])
