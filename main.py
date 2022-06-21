from pipeline.pipeline import Pipeline
from pipeline.steps.embedder.MPEmbedder import MPEmbedder
from pipeline.steps.evaluation.videoevaluation import VideoEvaluation
from pipeline.steps.input.googledriveservice import GoogleDriveService
from pipeline.steps.prediction.videoprediction import VideoPrediction
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.steps.training.videotraining import VideoTrainer

if __name__ == "__main__":
    # model = model.load_model("model_best.h5")
    pipeline = Pipeline(
        steps=[GoogleDriveService(), VideoPreProcessor(), MPEmbedder(), VideoTrainer(), VideoPrediction(),
               VideoEvaluation()], model=None)
    pipeline.process()
