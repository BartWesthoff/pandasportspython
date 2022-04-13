import numpy as np

from pipeline.pipeline import Pipeline
from pipeline.steps.input.input import Input
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.steps.embedder.videoembedder import VideoEmbeder
from pipeline.utils.utils import Utils
from sklearn import svm
if __name__ == "__main__":
    # Data inladen (misschien een stap weet ik nog niet)
    # data = ""

    # Pipeline (reeks van stappen) aanmaken
    # pipeline = Pipeline(Input())

    # Pipeline starten
    # pipeline.process(data)

    # De volgende classes zijn abstract en kunnen dus niet los aangemaakt worden.
    # PreProcessor()
    # Embedder()
    # Output()
    # Training()
    # Step()

    # De volgende classes zijn *niet* abstract en kunnen dus aangemaakt worden.
    # Als bij step.__init__(), self.__class__ was vergeleken zou het altijd true zijn
    # want VideoPreProcessor() == VideoPreProcessor() is altijd true
    # step = VideoPreProcessor()

    # krijg naam van een stap (class naam)

    # print(step.name)

    # Een pose genereren
    # pose2 = Utils().generatePose()

    # pose naar dictionary opslaan
    # print(pose2.ToJson())

    # get every joint from video

    # format: [
    #           [   x0,y0,z0,x1,y1,z1   ], #frame 1
    #           [   x0,y0,z0,x1,y1,z1   ], #frame 2
    #         ]

    allframes = VideoEmbeder().process("school video.mp4")
    #allframes = Utils().openObject("framestest")
    # print(allframes)
    array = np.array(allframes) # (137,99) (frames, joints*3)

   # data = np.reshape(array, (1,137, 99, 1))  # Here we have a total of 10 rows or records

    print(array.shape)
    # X = [[0, 0], [1, 1]]
    # y = [0, 1]
    # clf = svm.SVC()
    # clf.fit(X, y)
    # something = clf.predict([[0., 0.]])
    # print(something)



    Utils().playground()