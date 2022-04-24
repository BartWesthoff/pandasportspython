import numpy as np

from pipeline.pipeline import Pipeline
from pipeline.steps.input.input import Input
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.steps.embedder.videoembedder import VideoEmbeder
from pipeline.steps.training.videoTrainer import VideoTrainer
from pipeline.utils.utils import Utils
from sklearn import svm

if __name__ == "__main__":
    VideoTrainer().process("school video.mp4")




    # squads = Utils().openObject("framestest")
