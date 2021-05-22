import pickle
from CustomTransformer import TextCleaner, cleanText

class Classifier :
    
    def __init__(self, model_path):
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)

    def getSentiment(self, comments):

        """
        Returns pct bullishness in batch of comments passed in
        """

        predictions = self.model.predict(comments)
        bull = 0
        bear = 0
        neutral = 0
        for p in predictions:
            if p == "Bear":
                bear += 1
            elif p == "Bull":
                bull += 1
            else:
                neutral += 1
        bullishness = round((bull / (bull + bear)), 2)
        return bullishness