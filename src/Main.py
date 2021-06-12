import UI, Scraper, Classifier
from CustomTransformer import cleanText, TextCleaner
from datetime import datetime

if __name__ == "__main__":
    try:
        text_ui = UI.UI("Model/model.pk")
        text_ui.run()
    except:
        pass
    

    