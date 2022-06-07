import os

from pipeline.pipeline import Pipeline
from pipeline.steps.embedder.MPEmbedder import MPEmbedder
from pipeline.steps.input.dropboxservice import DropBoxService
from pipeline.steps.input.googledriveservice import GoogleDriveService
from pipeline.steps.training.videotraining import VideoTrainer
from pipeline.utils.utils import Utils

if __name__ == "__main__":

    VideoTrainer().process2()
    # for i in os.listdir(os.sep.join(['data', 'embedded'])):
    #     squat = Utils().openEmbedding(i)
    #     print(squat.shape)


