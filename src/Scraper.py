import requests

class Scraper :
    
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
    
    def getRequestResponse(self, url):
        """
        Takes in url and returns list of comments or Error
        """
        req_data = requests.get(url, headers={'User-agent': 'rtst.com'})
        if req_data.status_code == 200:
            json_data = req_data.json()
            return self.__parseChildren(json_data)
        else:
            return "Error"
    