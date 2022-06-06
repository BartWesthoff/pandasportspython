from __future__ import print_function

from pipeline.pipeline import Pipeline
from pipeline.steps.embedder.MPEmbedder import MPEmbedder
from pipeline.steps.input.dropboxservice import DropBoxService

if __name__ == "__main__":
    pipeline = Pipeline(steps=[DropBoxService(), MPEmbedder()], model=None)
    pipeline.process()
