from pipeline.pipeline import Pipeline
from pipeline.steps.preprocessors.preprocessor import PreProcessor
from pipeline.utils.utils import Utils

if __name__ == "__main__":
    # Utils().ensure_pythonhashseed(4)
    data = ""
    pipeline = Pipeline(PreProcessor())
    pipeline.process()
    pose2 = Utils().generatePose()
    print(pose2.ToJson())
# 46.832