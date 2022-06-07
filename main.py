from pipeline.pipeline import Pipeline
from pipeline.steps.embedder.MPEmbedder import MPEmbedder
from pipeline.steps.input.dropboxservice import DropBoxService
from pipeline.steps.input.googledriveservice import GoogleDriveService
from pipeline.utils.utils import Utils

if __name__ == "__main__":
    pipeline = Pipeline(steps=[GoogleDriveService(), MPEmbedder()], model=None)
    pipeline.process()



