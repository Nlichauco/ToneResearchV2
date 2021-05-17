import random
import csv
import os
import pandas as pd
from natsort import natsorted
import requests
from bs4 import BeautifulSoup

"""Count how many articles we have filtered in phrase one and phrase two
    Args:
        path: The path of the raw data
    Returns:
         No value returned, but print the total number of articles, number of articles filtered in phrase 1, and number 
         of articles filtered in phrase 2
    """


def count_percentage(path):
    missing_values = ["NaN", "0"]
    count_all = 0
    count_phrase1 = 0
    count_phrase2 = 0
    for filename in natsorted(os.listdir(path), key=lambda y: y.lower()):
        if not filename.startswith('.'):
            with open(os.path.join(path, filename)) as f:
                se = set()
                data = pd.read_csv(f, header=0, sep=r'\s*,\s*', na_values=missing_values, engine='python',
                                   usecols=[0, 1, 2, 5, 6, 7, 8, 9, 10, 11])

                for ind in data.index:
                    count_all += 1
                    url = data["URL"][ind]
                    if not clean(url) and url not in se:
                        se.add(url)
                        count_phrase1 += 1
                        if not phrase2(url):
                            count_phrase2 += 1
    print(count_all)
    print(count_phrase1)
    print(count_phrase2)


"""Decide whether given article will be filtered in Phrase 1 filtering
    Args:
        url: The url of the article
    Returns:
         True if the article will be filtered, False otherwise
    """


def phrase1(url):
    return ('coronavirus' not in url and 'covid' not in url and 'virus' not in url and 'pandemic' not in url
            and 'vaccine' not in url)


"""Decide whether given NYT article will be filtered in Phrase 2 filtering
    Args:
        url: The url of the article
    Returns:
         True if the article will be filtered, False otherwise
    """


def NYTPhrase2(url):
    return 'interactive' in url or 'photo' in url or 'video' in url or "podcast" in url or "quotation-of-the-day" in url


"""Decide whether given Guardian article will be filtered in Phrase 2 filtering
    Args:
        url: The url of the article
    Returns:
         True if the article will be filtered, False otherwise
    """


def GuardianPhrase2(url):
    return 'interactive' in url or "picture" in url or "photo" in url or "video" in url \
           or "music" in url or "book" in url or "share" in url


def main():
    # sum, dupe = Get_cut('res/Guardian/nodesk')
    # print("number of short articles: ", sum, "\n")
    # print("number of duplicate articles: ", dupe)

    # count_effective('out2.txt')
    # count_effective('out3.txt')

    count_percentage('res/NYT/nodesk')


main()
