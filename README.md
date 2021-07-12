# Real-Time-Sentiment-Tracker

A tool to track general market sentiment and performance over time. Use the data to make better or worse investing decisions. Happy gambling and I do not take any responsibilty for any bad trades made using this data =) 🚀🚀🚀🚀🚀

## Summary

There are 3 components of this tool.

1. Model Development
2. Scraping Service
3. Web Service

### Model Development
Contains ~1800 comments (.csv) scraped from the web that are labelled as bearish, bullish or neutral. The jupyter notebook contains training process and performance metrics.

### Scraping Service
The scraping module contains a standalone script to scrape comments from the web. The data is stored into AWS RDS. Deployed on AWS EC2 instance as a cronjob.

### Web Service
Flask backend contains 3 end points:
* /data -> returns time, sentiment, S&P500 price
* /performance -> returns historical performance of shorting vs going long on the S&P500 using the sentiment indictor. Also, returns accuracy (how often is the overnight sentiment indicative of positive/negative close the next day)
* /mentions -> counts of the top 5 tickers mentioned overnight

React frontend displays performance and mentions and a graph that shows historical sentiment and S&P500 closing price.
