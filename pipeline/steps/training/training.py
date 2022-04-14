from pipeline.steps.step import Step

"""
abstract training class
inherited by every trainer
"""

"""
NOTE: denk ik niet nodig want trainen gebeurt met model.fit maar dit is wel een stap in het process.
//TODO: even overleggen hoe we dit gaan aanpakken.
"""

# Moet nog gedaan worden
class Training(Step):

    def __init__(self):
        super().__init__(Training)

    def process(self, data):
        pass
