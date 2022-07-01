import tensorflow as tf

from pipeline.pipeline import Pipeline
from pipeline.steps.embedder.MPEmbedder import MPEmbedder
from pipeline.steps.evaluation.videoevaluation import VideoEvaluation
from pipeline.steps.input.googledriveservice import GoogleDriveService
from pipeline.steps.prediction.videoprediction import VideoPrediction
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.steps.training.videotrainer import VideoTrainer
from pipeline.steps.input.youtubeservice import YoutubeService
import sys

if __name__ == "__main__":
    def mode_one():
        model = tf.keras.models.load_model("custommodel42000train.h5")
        steps = [YoutubeService(), VideoPreProcessor(), MPEmbedder(), VideoTrainer(), VideoPrediction(),
                VideoEvaluation()]
        pipeline = Pipeline(
            steps=steps, model=model)
        pipeline.process()

    def mode_two():
        model = tf.keras.models.load_model("baselinemodel42000train.h5")
        steps = [YoutubeService(), VideoPreProcessor(), MPEmbedder(), VideoTrainer(), VideoPrediction(),
                VideoEvaluation()]
        pipeline = Pipeline(
            steps=steps, model=model)
        pipeline.process()

    def mode_three():
        steps = [YoutubeService(), VideoPreProcessor(), MPEmbedder(), VideoTrainer(), VideoPrediction(),
                VideoEvaluation()]
        pipeline = Pipeline(
            steps=steps, model=None)
        pipeline.process()

    if len(sys.argv) == 1:
        print('python main.py [ARG]\n\nARG = 1: Run optimized model\nARG = 2: Run baseline model\nARG = 3: Train your own model')
    else:
        if sys.argv[1] == "1":
            mode_one()
        elif sys.argv[1] == "2":
            mode_two()
        elif sys.argv[1] == "3":
            mode_three
        else:
            print('python main.py [ARG]\n\nARG = 1: Run optimized model\nARG = 2: Run baseline model\nARG = 3: Train your own model')