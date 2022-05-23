from classes.cloudfile import CloudFile
from pipeline.steps.embedder.videoembedder import VideoEmbeder
from pipeline.steps.input.input import GoogleDriveService
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.utils.utils import Utils

if __name__ == "__main__":
    GoogleDriveService().process()
