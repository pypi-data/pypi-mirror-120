class CaptureTimeout:
    pass

class StandByEvent:
    pass

class FrPipelineRequest:
    def __init__(self, user_result_callback=None, extra_params=None) -> None:
        self.user_result_callback = user_result_callback
        self.extra_params = extra_params

class StreamingRequest:
    def __init__(self) -> None:
        pass

class DetectionRequest:
    def __init__(self, frame, distance: int) -> None:
        self.distance = distance
        self.frame = frame

class RecognitionRequest:
    def __init__(self, frame, distance, bbox, cropped, ratio) -> None:
        self.frame, self.distance, self.bbox, self.cropped, self.ratio = frame, distance, bbox, cropped, ratio

class DisplayRequest:
    def __init__(self, frame, distance, bbox, cropped, ratio, user) -> None:
        self.frame, self.distance, self.bbox, self.cropped, self.ratio, self.user = frame, distance, bbox, cropped, ratio, user
        pass

class StreamingResult:
    def __init__(self, frame, range) -> None:
        self.frame = frame
        self.range = range

class DataFetched:
    def __init__(self):
        pass