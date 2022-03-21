from pipeline.pipeline import Pipeline
from pipeline.steps.preprocessors.preprocessor import PreProcessor


if __name__ == "__main__":
    #Helper().ensure_pythonhashseed(4)
    data = ""

    # pipeline = Pipeline(PreProcessor(), D2V(), SVM(), ApiOutput())
    print("hi")
    pipeline = Pipeline(PreProcessor())
    pipeline.process()

    # Example 3. Plotter and settings example
    # settings = Helper().load_yaml()
    # args = settings['pipeline']['combination']
    # d2v = args['d2v']
    # svm = args['svm']
    # pipeline = Pipeline(PreProcessor(), D2V(**d2v), SVM(**svm),
    #                     StatsOutput())
    #
    # outcome = pipeline.process(set(data))

