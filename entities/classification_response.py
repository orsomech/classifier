
class ClassificationResponse():
    def __init__(self, probability, correlation_id, error=None):
        self.probability = probability
        self.correlation_id = correlation_id
        self.error = error