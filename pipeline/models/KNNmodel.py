from random import *

import numpy as np
from sklearn import svm

from pipeline.models.model import Model
from pipeline.utils.utils import Utils


class SVMModel(Model):

    def fit(self):
        X = [np.array(Utils().generatePoseList(10, 10)).reshape(1, 900)[0] for _ in range(0, 40)]
        y = [randint(0, 100000) for _ in range(0, 40)]

        clf = svm.SVC()
        clf.fit(X, y)

        return clf
