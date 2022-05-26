import os
from random import *

import numpy as np
from sklearn import svm
from sklearn.svm import SVC

from pipeline.steps.embedder.thubembedder import ThubEmbedder
from pipeline.steps.input.input import GoogleDriveService
from pipeline.steps.training.videotraining import VideoTrainer
from pipeline.utils.utils import Utils

if __name__ == "__main__":
    #VideoTrainer().process('')
    # clf = Utils.openObject('SVMmodel')
    # for i in range(0, 100):
    #     array = np.array(Utils().generatePoseList(10, 10)).reshape(1, 900)
    #     print(clf.predict(array)[0], end=" ")
    #

    #
    # squat = ThubEmbedder().process(os.sep.join([Utils().datafolder, '20220330_121948_Trim5.mp4']))
    # # squat to numpy array
    # array = np.array(squat)
    # Utils().saveObject(array, 'squatTFHUB')


    squat = Utils().openObject('squatTFHUB')
    print(squat.shape)
    squat2 = squat.ravel()
    print(squat2.shape)
    model = SVC()
    model.fit([squat2,squat2], [0,1])
    answer = model.predict([squat2])
    print(answer)






