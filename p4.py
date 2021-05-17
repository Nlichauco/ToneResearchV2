import os
import pandas as pd
from natsort import natsorted

"""Count the total tone scores of the 7 tones
    Args:
        path: The path of the raw data (Covid NYT or Covid Guardian)
    Returns:
         An array contains the sum of every tone, listed in sequence: [Analytical, Sad, Confidence, Anger, Tentative, Fear, Joy] 
    """


def covid_count(path):
    res = [0, 0, 0, 0, 0, 0, 0]
    total = 0
    filter = 0
    for filename in natsorted(os.listdir(path), key=lambda y: y.lower()):
        if not filename.startswith('.'):
            with open(os.path.join(path, filename)) as f:
                se = set()
                data = pd.read_csv(f)

                for ind in data.index:
                    url = data["URL"][ind]
                    total += 1
                    if not cleanNYT(url) and url not in se:
                        filter += 1
                        se.add(url)
                        if data['Analy'][ind] > 0.5:
                            res[0] += 1
                        if data['Sad'][ind] > 0.5:
                            res[1] += 1
                        if data['Confi'][ind] > 0.5:
                            res[2] += 1
                        if data['Anger'][ind] > 0.5:
                            res[3] += 1
                        if data['Tenta'][ind] > 0.5:
                            res[4] += 1
                        if data['Fear'][ind] > 0.5:
                            res[5] += 1
                        if data['Joy'][ind] > 0.5:
                            res[6] += 1

    print(total)
    print(filter)
    return res


"""Phrase 1 + Phrase 2 filtering for NYT articles
    Args:
        url: The url of the article
    Returns:
         True if the article will be filtered, False otherwise
    """


def cleanNYT(url):
    return ('coronavirus' not in url and 'covid' not in url and 'virus' not in url and 'pandemic' not in url
            and 'vaccine' not in url) or 'interactive' in url or "picture" in url or "photo" in url or "movie" in url \
           or "music" in url or "book" in url or "share" in url


"""Phrase 1 + Phrase 2 filtering for Guardian articles
    Args:
        url: The url of the article
    Returns:
         True if the article will be filtered, False otherwise
    """


def cleanGuardian(url):
    return ('coronavirus' not in url and 'covid' not in url and 'virus' not in url and 'pandemic' not in url
            and 'vaccine' not in url) or 'interactive' in url or 'photo' in url or 'video' in url or "podcast" in url or "quotation-of-the-day" in url


"""Count the total tone scores of the 7 tones
    Args:
        path: The path of the raw data (H1N1 NYT or H1N1 Guardian)
    Returns:
         An array contains the sum of every tone, listed in sequence: [Analytical, Sad, Confidence, Anger, Tentative, Fear, Joy] 
    """


def h1n1_count(path):
    res = [0, 0, 0, 0, 0, 0, 0]
    total = 0
    for filename in natsorted(os.listdir(path), key=lambda y: y.lower()):
        if not filename.startswith('.'):
            with open(os.path.join(path, filename)) as f:
                data = pd.read_csv(f)

                for ind in data.index:
                    total += 1

                    if data['Analy'][ind] > 0.5:
                        res[0] += 1
                    if data['Sad'][ind] > 0.5:
                        res[1] += 1
                    if data['Confi'][ind] > 0.5:
                        res[2] += 1
                    if data['Anger'][ind] > 0.5:
                        res[3] += 1
                    if data['Tenta'][ind] > 0.5:
                        res[4] += 1
                    if data['Fear'][ind] > 0.5:
                        res[5] += 1
                    if data['Joy'][ind] > 0.5:
                        res[6] += 1
    print(total)
    return res


print(h1n1_count("res/H1N1/Guardian"))
