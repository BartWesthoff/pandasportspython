class Pose:

    def __init__(self, joints):
        self.joints = joints

    def ToJson(self):
        _dict = {}
        for joint in self.joints:
            _dict[joint.name] = {
                "x": joint.x,
                "y": joint.y,
                "z": joint.z,
                "likelihood": joint.likelihood
            }
        return _dict
