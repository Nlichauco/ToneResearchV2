import csv
import json
from datetime import date


import requests
from bs4 import BeautifulSoup
from requests.exceptions import SSLError

from GetDate import get_date_nyt_format
from ToneAnalyzer import tone_analyze
from entity.Article import Article


"""
    Checks each week for the amount of articles, if there are enough articles each one will be scored and added to a csv for that week.

    

    Args:
        que: An api query
        file_name: date range for the week queried

    Returns: The number of results on the page returned from the API. 
         """

def fetch_from_nyt(que, file_name):
    urls, articles, amt = pull(que)
    if amt < 1:
        # If there are no articles returned skip to the next week.
        return amt
    print("before get text")
    texts = get_text(urls)
    print("before create_arts")
    articles = create_arts(articles, texts)
    create_csv(articles, file_name)
    return amt


# Pull basic info from Guardian API, return url and list of article class OBJS


"""Api request, pulls important metadata.

    Pull() grabs the source, publication date and url of the articles returned.

    Args:
        que: An api query

    Returns:
         A list of urls, and a list of article class objects, the number of responses(articles in json) is also returned
         to check for 0 results"""


def pull(que):
    response = requests.get(que)
    news_json = response.json()
    print(news_json)
    resp = len(news_json['response']['docs'])
    arts = list()
    urls = []
    if resp == 0:
        return urls, arts, resp
    print(resp)

    for article in news_json['response']['docs']:
        source = article['source']
        date = article['pub_date']
        url = article['web_url']
        urls.append(url)
        arts.append(Article(source, date, url))

    return urls, arts, resp


"""Grabs text from websites, specifically Guardian

    Args:
        urls: urls is a url or list of urls.

    Returns:
        One array of plain text from each url."""


def get_text(urls):
    session = requests.Session()
    blob = []
    for url in urls:
        text = ""
        try:
            req = session.get(url)
        except SSLError:
            continue
        soup = BeautifulSoup(req.text, 'html.parser')
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            words = p.get_text()
            if len(text) + len(words) > 131069:
                break
            text = text + " " + words
        blob.append(text)
    print("end of for-loop get_text")
    return blob


"""Creates complete article class objects with tone scores

    Args:
        articles: article class objs each of which associates to a blob of text
        texts: A list of text blobs for the Tone Analyzer

    Returns:
         A list of article objects which also have tone scores."""


def create_arts(articles, texts):
    count = 0
    for text in texts:
        article = articles[count]
        tone_analyze(article, text)
        count += 1
    return articles


"""
Reads through article class objs and creates CSV for that week.

Args:
    articles: List of articles from the same week.
    file_name: desired name of CSV.
    scores: Scores from lexicon.

Returns:
    Nothing, creates file in directory"""


def create_template(file_name):
    with open(file_name, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Source", "Date", "URL", "Score", "   ", "Anger", "Fear", "Joy", "Sad", "Analy", "Confi", "Tenta"])

"""

    Appends each article with all tone scores to the template created for that week. 

    Args:
        articles: the articles objects for that week, each object holds all corresponding tone scores 
        file_name: the name of the file to append to. 

    Returns:
         A list of urls, and a list of article class objects, the number of responses(articles in json) is also returned
         to check for 0 results"""

def create_csv(articles, file_name):
    with open(file_name, 'a') as file:
        writer = csv.writer(file)
        for a in articles:
            writer.writerow(
                [a.source, a.published, a.url, 0, " ", a.anger, a.fear, a.joy, a.sadness, a.analytical,
                 a.confidence, a.tentative])


def demo():
    s_dates = get_date_nyt_format(0, date(2020, 12, 27), date(2021, 1, 2))
    e_dates = get_date_nyt_format(6, date(2020, 12, 27), date(2021, 1, 2))
    for i in range(0, len(s_dates)):
        file_name = "2020-" + s_dates[i][:2] + "-" + s_dates[i][2:] + ".csv"
        page = 0
        create_template(file_name)
        while 1:
            que = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=coronavirus&page=" + str(page) + \
                  '&fq=news_desk:("Sports")&source:("The New York Times")&facet=true&sort=relevance&begin_date=2020' + \
                  s_dates[i] + "&end_date=2021" + e_dates[i] + "&api-key=JGcjpWJ6Yc9UcW7TepoAbnqbHrR5tGAW"
            if fetch_from_nyt(que, file_name) != 10:
                break
            page += 1


demo()
