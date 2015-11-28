import csv
from company import Company

#self, name, status, market, country, funding_value, funding_rounds):
def parseData(csvfile):
    with open(csvfile, 'rb') as data_file:
        data_reader = csv.reader(data_file, delimiter=',', quotechar='"')
        comp_arr = []
        country_totals = {}
        market_totals = {}
        country_weights = {}
        market_weights = {}
        num = 0

        for line in data_reader:
            if (num > 0):
                comp_arr.append(Company(line[0], line[3], line[1], line[4], line[2], line[7]))

                ## Country map
                if (line[4] in country_totals):
                    if (company_success(line[3])):
                        country_totals[line[4]][0] += 1
                    else:
                        country_totals[line[4]][1] += 1
                else:
                    if (company_success(line[3])):
                        country_totals[line[4]] = [1,0]
                    else:
                        country_totals[line[4]] = [0,1]

                ## Market map
                if (line[1] in market_totals):
                    if (company_success(line[3])):
                        market_totals[line[1]][0] += 1
                    else:
                        market_totals[line[1]][1] += 1
                else:
                    if (company_success(line[3])):
                        market_totals[line[1]] = [1,0]
                    else:
                        market_totals[line[1]] = [0,1]

            for country in country_totals:
                if (country_totals[country][1] > 0):
                    country_weights[country] = float(country_totals[country][0])/float(country_totals[country][1]) * 10
                else:
                    country_weights[country] = 2

            for market in market_totals:
                if (float(market_totals[market][1]) > 0):
                    market_weights[market] = float(market_totals[market][0])/float(market_totals[market][1]) * 10
                else:
                    market_weights[market] = 2
            num += 1

    return comp_arr, country_weights, market_weights

def company_success(status):
    if (status in ('ipo', 'aquired')):
        return True
    return False

