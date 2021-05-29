import Scraper, Classifier
import time

class UI :

    def textUI(self):

        """
        Simple text visualization of sentiment over time
        """
        s = Scraper.Scraper()
        text_classifier = Classifier.Classifier("Model/model.pk")
        print("%20s %20s" % ("Time", "Sentiment"))
        while True:
            now = time.strftime("%H:%M:%S")
            comments = s.getRequestResponse()
            if comments == "ERROR":
                time.sleep(3)
                continue
            sentiment = text_classifier.getSentiment(comments)
            print("%20s %20s" % (now, sentiment))
            time.sleep(60)



