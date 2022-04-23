import numpy as np

from classes.cloudfile import CloudFile
from pipeline.steps.embedder.videoembedder import VideoEmbeder
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.utils.utils import Utils

if __name__ == "__main__":
    # frames = Utils().openObject("voorbeeld")
    frames = VideoEmbeder().process("school video.mp4")
    Utils().saveObject(frames, "frames test")
    file = CloudFile(id="", name="20220330_112652_short.mp4", parents="")
    VideoPreProcessor().process([file])

    # frames = VideoEmbeder().process("result2.mp4")
    #
    # Utils().saveObject(frames, "frames kleur")
    # convert array to numpy array

    # squat = Utils().augmentation(frames[0], 20)
    # for i in squat:
    #     print(i[0])
    # VideoPreProcessor().showvideo(f"{Utils().datafolder + os.sep}20220330_121747.mp4")
    # VideoPreProcessor().cropVideo("20220330_112652_short.mp4", 30)
    # Utils().playground()
