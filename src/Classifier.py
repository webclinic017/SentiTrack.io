import pickle
from CustomTransformer import TextCleaner, cleanText
import datetime

class Classifier :
    
    def __init__(self, model_path):
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)
    
    def __getScore(self, predictions):

        """
        Returns sentiment score (between -1 to 1) for the interval.
        """
        score = 0
        comments = 0
        for prediction in predictions:
            if prediction == "Bull":
                score += 1
                comments += 1
            elif prediction == "Bear":
                score -= 1
                comments +=1
        return round(score/comments, 2)


    def getSentiment(self, range_map):

        """
        Returns sentiment score for each interval in range map
        """
        data = {}
        for interval in range_map:
            predictions = self.model.predict(interval[1])
            score = self.__getScore(predictions)
            data[datetime.datetime.strftime(interval[0][1], '%H:%M:%S')] = score
        return data


        

