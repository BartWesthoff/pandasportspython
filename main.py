import numpy as np

from pipeline.pipeline import Pipeline
from pipeline.steps.input.input import Input
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.steps.embedder.videoembedder import VideoEmbeder
from pipeline.utils.utils import Utils
from sklearn import svm

if __name__ == "__main__":
    # Data inladen (misschien een stap weet ik nog niet)
    data = ""

    # Pipeline (reeks van stappen) aanmaken
    pipeline = Pipeline(Input())

    # Pipeline starten
    pipeline.process(data)

    # Resultaat uit de pipeline halen
