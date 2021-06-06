import requests
import datetime
import time
from DateTimeRangeMap import DateTimeRangeMap
import threading

class Scraper :

    def __getUrl(self, url):

        """
        Returns response from url
        """

        return requests.get(url, headers={'User-agent': 'rtst.com'})

    def __getCurrentDiscussionThreadURL(self):

        """
        Fetches endpoint of current/active discussion thread
        """

        base_url = "https://www.reddit.com"
        front_page = "https://www.reddit.com/r/wallstreetbets/.json"
        req_data = self.__getUrl(front_page)
        if req_data.status_code != 200:
            return "ERROR"
        #active discussion is always pinned at top
        json_response = req_data.json()
        url = base_url + json_response['data']['children'][0]['data']['permalink'] + ".json"
        return url

    def __getComments(self, json_response, now, historical, interval = 5.0):

        """
        Parses json response and returns map of comments within the last interval
        If historical = True, returns map of comments for each interval from past hour
        """

        now = now.replace(second = 0, microsecond = 0)
        range_map = DateTimeRangeMap(now, interval, historical)
        children = json_response[1]['data']['children']
        for child in children:
            if child['kind'] == 'more' and historical:
                # rest of comments are represented as list of comment ids
                children = child['data']['children']
                extra_comments_ids  = [c for c in children]  
            else :
                try:
                    comment = child['data']['body']
                    if comment == '[removed]':
                        continue
                    time = int(child['data']['created_utc'])
                    time = datetime.datetime.fromtimestamp(time).replace(second = 0, microsecond = 0)
                    range_map.insert(time, comment)              
                except: KeyError
        range_map = self.__makeRequestsForExtraComments(extra_comments_ids, range_map)
        return range_map
    
    def getRequestResponse(self, time, historical = False):

        """
        Takes in url and returns latest batch of comments
        """
        
        url = self.__getCurrentDiscussionThreadURL()
        if url == "ERROR":
            return url
        req_data = self.__getUrl(url)
        if req_data.status_code == 200:
            json_data = req_data.json()
            return self.__getComments(json_data, time, historical)
        else:
            return "ERROR"


    def __updateMap(self, url, range_map):

        """
        Given url update the range_map with comment in the respective time interval
        """

        response = self.__getUrl(url)
        if response.status_code == 200:
            req_data = response.json()
            try :
                data = req_data['data']['children'][0]['data']
                comment = data['body']
                if comment == '[removed]':
                    return
                time = int(data['created_utc'])
                time = datetime.datetime.fromtimestamp(time).replace(second = 0, microsecond = 0)
                range_map.insert(time, comment)
            except:
                pass
            
    def __makeRequestsForExtraComments(self, list_of_comment_ids, range_map):

        """
        Updates DateTimeRangeMap with data from the extra comments
        """
        base_url = "https://www.reddit.com/api/info.json?id=t1_"
        urls = [base_url + id for id in list_of_comment_ids]

        threads = [threading.Thread(target = self.__updateMap, args=(url,range_map)) for url in urls]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return range_map


        


