import csv

import pandas as pd

"""Creates an list of rolling 7 day averages for plotting

    Args:
        filename: name of csv file you would like to read

    Returns:
         A list of covid case numbers."""


def get_avg_daily_cases(filename):
    avg = []
    count = 0
    my_sum = 0
    with open(filename) as f:
        data = pd.read_csv(f, header=0)
        for ind in data.index:
            count += 1
            my_sum += data["new_cases"][ind]
            if count == 7:
                avg.append(my_sum / 7)
                count = 0
                my_sum = 0

    with open("res/CovidData/UKcovidAVG.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["cases"])
        for num in avg:
            writer.writerow([int(num)])


get_avg_daily_cases("uk.csv")
