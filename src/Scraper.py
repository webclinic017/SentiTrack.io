import requests

class Scraper :

    def __getCurrentDiscussionThreadURL(self):

        """
        Fetches endpoint of current/active discussion thread
        """

        base_url = "https://www.reddit.com"
        front_page = "https://www.reddit.com/r/wallstreetbets/.json"
        req_data = requests.get(front_page, headers={'User-agent': 'rtst.com'})
        if req_data.status_code != 200:
            return "ERROR"
        #active discussion is always pinned at top
        json_response = req_data.json()
        url = base_url + json_response['data']['children'][0]['data']['permalink'] + ".json"
        return url

    def __parseChildren(self, json_response):

        """
        Parses json response and returns list of comments
        """

        comments = []
        children = json_response[1]['data']['children']
        for child in children:
            try:
                comment = child['data']['body']
                comments.append(comment)
            except: KeyError
        return comments
    
    def getRequestResponse(self):

        """
        Takes in url and returns list of comments or Error
        """
        url = self.__getCurrentDiscussionThreadURL()
        if url == "ERROR":
            return url
        req_data = requests.get(url, headers={'User-agent': 'rtst.com'})
        if req_data.status_code == 200:
            json_data = req_data.json()
            return self.__parseChildren(json_data)
        else:
            return "ERROR"