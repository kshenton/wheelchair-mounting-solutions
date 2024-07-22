class Wheelchair:
    def __init__(self, model, frame_clamps, mount_location):
        self.model = model
        self.frame_clamps = frame_clamps
        self.mount_location = mount_location

class AACDevice:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

class Mount:
    def __init__(self, name, weight_capacity):
        self.name = name
        self.weight_capacity = weight_capacity