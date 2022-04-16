from pipeline.pipeline import Pipeline
from pipeline.steps.evaluation.videoevaluation import VideoEvaluation
from pipeline.steps.input.input import Input
from pipeline.steps.output.videooutput import VideoOutput
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.steps.training.videotraining import VideoTraining

if __name__ == "__main__":
    # pipeline = Pipeline(Input(), VideoPreProcessor(), VideoTraining(), VideoEvaluation(), VideoOutput())
    # pipeline.process()

    #VideoPreProcessor().trimvideo("20220330_112652", 0.0, 11.0)

    VideoPreProcessor().crop("00:01:00", "00:01:09", "20220330_112652", "trimmedvideo")
    #VideoPreProcessor().trimvideo2("20220330_112652")