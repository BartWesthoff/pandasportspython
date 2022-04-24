import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from pipeline.steps.training.training import Training
from pipeline.utils.utils import Utils
import os

# Using linear regression because the datapoints have numerical values (xyz coords of joints) that need to be in proportion to one another. Makes linreg a good choice

class VideoTrainer(Training):
#    def process(self, data, labels):
        #data_train, data_test, labels_train, labels_test = train_test_split(
        #    data, labels, test_size=0.25, random_state=42)

        #LR = LinearRegression().fit(data, labels)
        #LR = LinearRegression().fit(data_train, labels_train)

        #prediction = LR.score(data, labels)
        #print(prediction)

    def process(self, data):
        labels = []
        utils = Utils()
        allFiles = os.listdir(utils.datafolder)

        for bestand in allFiles:
            print(bestand)
            if "positive" in bestand:
                labels.append(1)
            elif "negative" in bestand:
                labels.append(0)
            else:
                raise Exception("False names!")
        

        model = Utils.define_model()
        data = np.array(data)
        data = np.reshape(data, (len(labels), 137, 99))
        fitted = model.fit(data, np.array(labels), epochs=2, batch_size=2, verbose=1)
        Utils.saveObject(fitted, "fittedSequentialTestModel")