import requests
import datetime
import pymysql
import pickle
import json
from CustomTransformer import TextCleaner, cleanText

def getResponse(url):

    """
    Returns response from url
    """

    return requests.get(url, headers={'User-agent': 'rtst.com'})

def getCurrentDiscussionThreadURL():

    """
    Fetches endpoint of current/active discussion thread
    """

    base_url = "https://www.reddit.com"
    front_page = "https://www.reddit.com/r/wallstreetbets/.json"
    req_data = getResponse(front_page)
    if req_data.status_code != 200:
        return "ERROR"
    #active discussion is always pinned at top
    json_response = req_data.json()
    url = base_url + json_response['data']['children'][0]['data']['permalink'] + ".json"
    return url

def getComments(json_response):

    """
    Gets the comments within the last 5 minutes 
    """

    comments = []
    now = datetime.datetime.now().replace(second = 0, microsecond = 0)
    ten_minute = datetime.timedelta(minutes = 10)
    past = now - ten_minute
    children = json_response[1]['data']['children']
    for child in children:
        if child['kind'] == 'more':
            return comments
        else :
            try:
                comment = child['data']['body']
                if comment == '[removed]':
                    continue
                time = int(child['data']['created_utc'])
                time = datetime.datetime.fromtimestamp(time).replace(second = 0, microsecond = 0)
                if (time < past):
                    return  comments
                comments.append(comment)      
            except: KeyError
    return comments

def getScore(predictions):

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

def getSentiment(model_path, comments):

    """
    Returns sentiment for batch of comments
    """

    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    predictions = model.predict(comments)
    sentiment = getScore(predictions)
    return sentiment

if __name__ == "__main__":
    with open('config.json') as f:
        data = json.load(f)
    db = pymysql.connect(host = data['host'], 
                         user = data['user'], 
                         password = data['password'], 
                         database = data['database'])
    cursor = db.cursor()

    time = datetime.datetime.now()
    url = getCurrentDiscussionThreadURL()
    req_data = getResponse(url)
    json_data = req_data.json()
    comments = getComments(json_data)
    sentiment = getSentiment("model.pk", comments)

    cursor.execute('INSERT INTO WSB (LogTime, Sentiment) VALUES (%s, %s)', (time.strftime('%Y-%m-%d %H:%M:%S'), sentiment))
    db.commit()
    db.close()






        


