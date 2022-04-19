import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from pipeline.steps.training.training import Training

# Using linear regression because the datapoints have numerical values (xyz coords of joints) that need to be in proportion to one another. Makes linreg a good choice

class VideoTrainer(Training):
    def Train(self, data, labels):
        data_train, data_test, labels_train, labels_test = train_test_split(
            data, labels, test_size=0.25, random_state=42)
        LR = LinearRegression().fit(data_train, labels_train)

        prediction = LR.score(data_test, labels_test)
        print(prediction)