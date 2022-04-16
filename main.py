from pipeline.pipeline import Pipeline
from pipeline.steps.evaluation.videoevaluation import VideoEvaluation
from pipeline.steps.input.input import Input
from pipeline.steps.output.videooutput import VideoOutput
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.steps.training.videotraining import VideoTraining

if __name__ == "__main__":
    pipeline = Pipeline(Input(), VideoPreProcessor(), VideoTraining(), VideoEvaluation(), VideoOutput())
    pipeline.process()
