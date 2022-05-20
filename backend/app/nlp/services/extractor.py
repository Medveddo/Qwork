class FeatureExtractor:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            print("Initializing FeatureExtractor")
            cls.instance = super(FeatureExtractor, cls).__new__(cls)
        return cls.instance
