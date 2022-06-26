import os

from pipeline.pipeline import Pipeline
from pipeline.steps.embedder.MPEmbedder import MPEmbedder
from pipeline.steps.evaluation.videoevaluation import VideoEvaluation
from pipeline.steps.input.googledriveservice import GoogleDriveService
from pipeline.steps.prediction.videoprediction import VideoPrediction
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.steps.training.videotraining import VideoTrainer

if __name__ == "__main__":
    model = tf.keras.models.load_model("custommodel.h5")
    pipeline = Pipeline(
        steps=[GoogleDriveService(), VideoPreProcessor(), MPEmbedder(), VideoTrainer(), VideoPrediction(),
               VideoEvaluation()], model=model)
    pipeline.process()

    # count_positive = 0
    # count_negative = 0
    # for i in os.listdir(os.sep.join(["data", "embedded"])):
    #     if "negative" in i:
    #         # squat = Utils().openEmbedding(i)
    #         # squats = Utils().data_augmentation_normalized(amount=20, name=i, squat=squat, save=True)
    #         # print(squats.shape)
    #         count_negative += 1
    #     if "positive" in i:
    #         count_positive += 1
    # print(count_positive)
    # print(count_negative)
