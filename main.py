from pipeline.pipeline import Pipeline
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.utils.utils import Utils

if __name__ == "__main__":
    # Data inladen (misschien een stap weet ik nog niet)
    data = ""

    # Pipeline (reeks van stappen) aanmaken
    pipeline = Pipeline(VideoPreProcessor())

    # Pipeline starten
    pipeline.process(data)

    # De volgende classes zijn abstract en kunnen dus niet los aangemaakt worden.
    # PreProcessor()
    # Embedder()
    # Output()
    # Training()
    # Step()

    # De volgende classes zijn *niet* abstract en kunnen dus aangemaakt worden.
    # Als bij step.__init__(), self.__class__ was vergeleken zou het altijd true zijn
    # want VideoPreProcessor() == VideoPreProcessor() is altijd true
    step = VideoPreProcessor()

    # krijg naam van een stap (class naam)

    print(step.name)

    # Een pose genereren
    pose2 = Utils().generatePose()

    # pose naar dictionary opslaan
    print(pose2.ToJson())
