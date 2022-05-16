import numpy as np

from classes.cloudfile import CloudFile
from pipeline.steps.embedder.videoembedder import VideoEmbeder
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.utils.utils import Utils

if __name__ == "__main__":
    settings = Utils.load_settings()
    print(type(settings))  # <class 'dict'>
    print(settings)  # example: {'use_gpu': 0, 'use_local': 1}
