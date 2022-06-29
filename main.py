import tensorflow as tf

from pipeline.pipeline import Pipeline
from pipeline.steps.embedder.MPEmbedder import MPEmbedder
from pipeline.steps.evaluation.videoevaluation import VideoEvaluation
from pipeline.steps.input.googledriveservice import GoogleDriveService
from pipeline.steps.prediction.videoprediction import VideoPrediction
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.steps.training.videotrainer import VideoTrainer

if __name__ == "__main__":
    model = tf.keras.models.load_model("custommodel42000NG9train.h5")
    steps = [GoogleDriveService(), VideoPreProcessor(), MPEmbedder(), VideoTrainer(), VideoPrediction(),
             VideoEvaluation()]
    pipeline = Pipeline(
        steps=steps, model=None)  # testdata=False
    pipeline.process()
