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
