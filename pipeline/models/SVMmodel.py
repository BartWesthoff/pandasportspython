from random import *

import numpy as np
from sklearn import svm

from pipeline.models.model import Model
from pipeline.utils.utils import Utils


# Klasse voor het aanmaken van het SVMModel

class SVMModel(Model):



    def fit(self, x_train=None, y_train=None):  # tijdelijk omdat we nog geen data hebben
        X = [np.array(Utils().generatePoseList(10, 10)).reshape(1, 900)[0] for _ in range(0, 40)]
        # X = [np.array(Utils().generatePoseList(10, 10)).flatten() for _ in range(0, 40)]
        # TODO kijken of het werkt
        y = [randint(0, 100000) for _ in range(0, 40)]

        # clf = svm.SVC(**self.model_kwargs)
        clf = svm.SVC(kernel='linear')
        clf.fit(X, y)
        # clf.fit(x_train, y_train)

        return clf
    # TODO bij predicten kijken of aantal features gelijk is aan aantal features in de training set

    def predict(self, x_test):
        return self.model.predict(x_test)
