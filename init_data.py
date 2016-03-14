import csv
import datetime
from Company import Company

#self, name, status, market, country, city, funding_value, funding_rounds):
##TODO:
### Take the percentage closed vs. operating/acquired/ipo for values 50,000 - 100,000
#### Take how much funding they got per day for everyone > 100,000
#####
MONEYTHRESHOLD = 800000
def parseData(csvfile):
    with open(csvfile, 'rb') as data_file:
        next(data_file)
        data_reader = csv.reader(data_file, delimiter=',', quotechar='"')

        train_data = []
        test_data = []
        country_totals = {}
        city_totals = {}
        market_totals = {}
        country_weights = {}
        city_weights = {}
        market_weights = {}

        entry_num = 0

        for line in data_reader:
            if(int(line[2]) > 50000 and (line[8] != '' or line[9] != '')):
                if(int(line[2]) > 100000):
                    entry_num += 1

                    if (line[8] != '' and line[9] != ''):
                        d1a = datetime.date(int(line[9][:4]), int(line[9][5:7]), int(line[9][8:10]))
                        d1b = datetime.date(int(line[8][:4]), int(line[8][5:7]), int(line[8][8:10]))
                        if (d1a > d1b):
                            d1 = d1a
                        else:
                            d1 = d1b
                    else:
                        if (not line[8] or line[8] == ''):
                            d1 = datetime.date(int(line[9][:4]), int(line[9][5:7]), int(line[9][8:10]))
                        else:
                            d1 = datetime.date(int(line[8][:4]), int(line[8][5:7]), int(line[8][8:10]))

                    d2 = datetime.date(int(line[10][:4]), int(line[10][5:7]), int(line[10][8:10]))

                    delta = (d2 - d1).days
                    delta = 1 if (delta == 0) else abs(delta)
                    money_delta = int(line[2])/(float(delta) / 365.0)

                    if (entry_num % 50 != 0):
                        train_data.append(Company(line[0], line[3], line[1], line[4], line[6], line[2], line[7], money_delta))

                        ## Country map
                        if (line[4] in country_totals):
                            if (company_status(line[3], money_delta)):
                                country_totals[line[4]][0] += 1
                            else:
                                country_totals[line[4]][1] += 1
                        else:
                            if (company_status(line[3], money_delta)):
                                country_totals[line[4]] = [1,0]
                            else:
                                country_totals[line[4]] = [0,1]

                        ## Market map
                        if (line[1] in market_totals):
                            if (company_status(line[3], money_delta)):
                                market_totals[line[1]][0] += 1
                            else:
                                market_totals[line[1]][1] += 1
                        else:
                            if (company_status(line[3], money_delta)):
                                market_totals[line[1]] = [1,0]
                            else:
                                market_totals[line[1]] = [0,1]

                        #City Map
                        if (line[6] in city_totals):
                            if (company_status(line[3], money_delta)):
                                city_totals[line[6]][0] += 1
                            else:
                                city_totals[line[6]][1] += 1
                        else:
                            if (company_status(line[3], money_delta)):
                                city_totals[line[6]] = [1,0]
                            else:
                                city_totals[line[6]] = [0,1]
                    else:
                        test_data.append(Company(line[0], line[3], line[1], line[4], line[6], line[2], line[7], money_delta))

        for country in country_totals:
            if (country_totals[country][0] > 0):
                country_weights[country] = float(country_totals[country][1])/float(country_totals[country][0]) * 10 + 0.1
            else:
                country_weights[country] = 2

        for city in city_totals:
            if (city_totals[city][0] > 0):
                city_weights[city] = float(city_totals[city][1])/float(city_totals[city][0]) * 10 + 0.1
            else:
                city_weights[city] = 2

        for market in market_totals:
            if (float(market_totals[market][0]) > 0):
                market_weights[market] = float(market_totals[market][1])/float(market_totals[market][0]) * 10 + 0.1
            else:
                market_weights[market] = 2

    return train_data, test_data, country_weights, city_weights, market_weights

def company_status(status, money_delta):
    if (status in ('ipo', 'acquired', 'operating') and money_delta > MONEYTHRESHOLD):
        return True
    return False

