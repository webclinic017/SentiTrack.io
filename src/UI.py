import Scraper, Classifier
import art
import datetime
import time

class UI :

    def __init__(self, model_path):
        self.s = Scraper.Scraper()
        self.text_classifier = Classifier.Classifier(model_path)

    def __formatPrint(self, predictions):
        for t in sorted(predictions):
            print("%40s %20s" % (t,"%.2f" % predictions[t]))

    def run(self):

        """
        Simple text visualization of sentiment over time
        """

        print(art.text2art("SENTIMENT ANALYSIS", font="small"))
        print ("========================================================================================================")
        print ("========================================================================================================")
        t = datetime.datetime.now()
        past_hour_data = self.s.getRequestResponse(t, historical=True).getRangeMap()
        if past_hour_data is None:
            print("No past hour data available.")
        predictions = self.text_classifier.getSentiment(past_hour_data)
        print("%40s %20s" % ("Time", "Sentiment"))
        self.__formatPrint(predictions)
        while (True):
            time.sleep(300)
            t = datetime.datetime.now()
            data = self.s.getRequestResponse(t).getRangeMap()
            if data is None:
                continue
            predictions = self.text_classifier.getSentiment(data)
            self.__formatPrint(predictions)
        


        
            










