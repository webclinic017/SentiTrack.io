import requests
import datetime
import pymysql
import pickle
import json
from bs4 import BeautifulSoup
from CustomTransformer import TextCleaner, cleanText
import threading
from collections import Counter

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

def getMoreComments(url, comments):

        """
        Gets comment from url and updats list
        """

        response = getResponse(url)
        if response.status_code == 200:
            req_data = response.json()
            try :
                data = req_data['data']['children'][0]['data']
                comment = data['body']
                if comment == '[removed]':
                    return
                comments.append(comment)
            except:
                pass

def makeRequestsForExtraComments(list_of_comment_ids, comments):

        """
        Creates thread for each comment id and fetches comment
        """

        base_url = "https://www.reddit.com/api/info.json?id=t1_"
        urls = [base_url + id for id in list_of_comment_ids]

        threads = [threading.Thread(target = getMoreComments, args=(url, comments)) for url in urls]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return comments


def getComments(json_response):

    """
    Gets the comments within the last 5 minutes 
    """

    comments = []
    children = json_response[1]['data']['children']
    for child in children:
        if child['kind'] == 'more':
            children = child['data']['children']
            extra_comment_ids  = [c for c in children] 
        else :
            try:
                comment = child['data']['body']
                if comment == '[removed]':
                    continue
                comments.append(comment)      
            except: KeyError
    makeRequestsForExtraComments(extra_comment_ids, comments)
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

def getMarketPrice():
    url = "https://finance.yahoo.com/quote/SPY?p=SPY&.tsrc=fin-srch"
    res = getResponse(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        price = soup.find('span', {'data-reactid': '50'}).text
        return price
    else:
        return None

def getMentions(comments, tickers):

    """
    Return counts for all tickers mentioned
    """

    counts = {}
    comments = [comment.upper() for comment in comments]
    for comment in comments:
        for t in tickers:
            if t in comment.split():
                if t in counts:
                    counts[t] += 1
                else:
                    counts[t] = 1
    counts = Counter(counts)
    top = counts.most_common(5) 
    return json.dump(top)

        
if __name__ == "__main__":
    with open("ScrapingService/config.json") as f:
        data = json.load(f)
    market = getMarketPrice()
    if market is not None:
        market = float(market)

    time = datetime.datetime.now()
    url = getCurrentDiscussionThreadURL()
    req_data = getResponse(url)
    json_data = req_data.json()
    comments = getComments(json_data)

    sentiment = getSentiment("ScrapingService/model.pk", comments)

    db = pymysql.connect(host = data['host'], 
                         user = data['user'], 
                         password = data['password'], 
                         database = data['database'])
    cursor = db.cursor()
    cursor.execute('INSERT INTO WSB (LogTime, Sentiment, Market) VALUES (%s, %s, %s)', 
                    (time.strftime('%Y-%m-%d %H:%M:%S'), sentiment, market))

    with open('ScrapingService/tickers.txt') as f:
        tickers = list(f)
        tickers = [x.rstrip() for x in tickers]

    mentions = getMentions(comments, tickers)

    cursor.execute('INSERT INTO MENTIONS (LogTime, Ticker1, Ticker1_Count, \
                                                   Ticker2, Ticker2_Count, \
                                                   Ticker3, Ticker3_Count, \
                                                   Ticker4, Ticker4_Count, \
                                                   Ticker5, Ticker5_Count) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                                                  (time.strftime('%Y-%m-%d %H:%M:%S'),
                                                   mentions[0][0], mentions[0][1],
                                                   mentions[1][0], mentions[1][1],
                                                   mentions[2][0], mentions[2][1], 
                                                   mentions[3][0], mentions[3][1],
                                                   mentions[4][0], mentions[4][1]))
    db.commit()
    db.close()