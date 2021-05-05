import random
import csv
import os
import pandas as pd
from natsort import natsorted
import requests
from bs4 import BeautifulSoup


def Get_cutoff(path):
    sum = []

    missing_values = ["NaN", "0"]
    # print(os.listdir(path))

    for filename in natsorted(os.listdir(path), key=lambda y: y.lower()):

        if not filename.startswith('.'):
            # print(filename,"\n")

            with open(os.path.join(path, filename)) as f:

                numset = set()

                data = pd.read_csv(f, header=0, sep=r'\s*,\s*', na_values=missing_values, engine='python',
                                   usecols=[0, 1, 2, 5, 6, 7, 8, 9, 10, 11])
                length = len(data.index)

                if length <= 10:
                    for i in range(0, length):
                        articlelength = get_text(data['URL'][i])
                        sum.append(articlelength)
                else:
                    i = 0

                    while (i < 10):

                        number = random.randrange(0, length)

                        if number not in numset:
                            numset.add(number)
                            articlelength = get_text(data['URL'][number])
                            sum.append(articlelength)
                            i += 1
    sum.sort()
    listLen = len(sum)
    cutoff = int(.05 * listLen)

    return sum[cutoff]


def Get_cut(path):
    sum = 0
    dupe = 0
    outfile = open("out3.txt", "a")

    missing_values = ["NaN", "0"]
    # print(os.listdir(path))

    for filename in natsorted(os.listdir(path), key=lambda y: y.lower()):

        if not filename.startswith('.'):
            # print(filename,"\n")

            with open(os.path.join(path, filename)) as f:
                numset = set()

                data = pd.read_csv(f, header=0, sep=r'\s*,\s*', na_values=missing_values, engine='python',
                                   usecols=[0, 1, 2, 5, 6, 7, 8, 9, 10, 11])
                length = len(data.index)
                for i in range(0, length):
                    articlelength = get_text(data['URL'][i])
                    if articlelength < 500 and data['URL'][i] not in numset:
                        print("made it")
                        outfile.write(data['URL'][i] + "\n")
                        sum += 1
                        numset.add(data['URL'][i])
                    elif data['URL'][i] in numset:
                        dupe += 1

    return sum, dupe


def get_text(url):
    session = requests.Session()
    text = 0
    req = session.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        words = p.get_text()
        text += len(words)
    return text


def count_effective(file):
    count = 0
    count_total = 0
    with open(file, 'r') as f:
        for line in f:
            if clean(line):
                continue
            count_total += 1
            if "picture" in line or "photo" in line or "movie" in line or "music" in line or "book" in line or "share" in line:
                count += 1
    print(count_total)
    print(count)


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


def clean(url):
    return ('coronavirus' not in url and 'covid' not in url and 'virus' not in url and 'pandemic' not in url
            and 'vaccine' not in url)


def NYTclean(url):
    return (
                       'coronavirus' not in url and 'covid' not in url and 'virus' not in url and 'pandemic' not in url and 'vaccine' not in url) or 'interactive' in url or 'photo' in url or 'video' in url or "podcast" in url or "quotation-of-the-day" in url


def phrase2(url):
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
