import csv
from Company import Company

#self, name, status, market, country, city, funding_value, funding_rounds):
def parseData(csvfile):
    with open(csvfile, 'rb') as data_file:
        next(data_file)
        data_reader = csv.reader(data_file, delimiter=',', quotechar='"')

        comp_arr = []
        country_totals = {}
        city_totals = {}
        market_totals = {}
        country_weights = {}
        city_weights = {}
        market_weights = {}

        for line in data_reader:
            #print(line[2])
            if(line[2] > 0):
                comp_arr.append(Company(line[0], line[3], line[1], line[4], line[6], line[2], line[7]))
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

                #City Map
                if (line[6] in city_totals):
                    if (company_success(line[3])):
                        city_totals[line[6]][0] += 1
                    else:
                        city_totals[line[6]][1] += 1
                else:
                    if (company_success(line[3])):
                        city_totals[line[6]] = [1,0]
                    else:
                        city_totals[line[6]] = [0,1]


        for country in country_totals:
            if (country_totals[country][0] > 0):

                country_weights[country] = float(country_totals[country][1])/float(country_totals[country][0]) * 10
            else:
                country_weights[country] = 2

        for city in city_totals:
            if (city_totals[city][0] > 0):
                city_weights[city] = float(city_totals[city][1])/float(city_totals[city][0]) * 10
            else:
                city_weights[city] = 2

##TODO: MAKE TOTALS INTO WEIGHTS
### DO WEIGHTS FOR MARKET

        for market in market_totals:
            if (float(market_totals[market][0]) > 0):
                market_weights[market] = float(market_totals[market][1])/float(market_totals[market][0]) * 10
            else:
                market_weights[market] = 2

    return comp_arr, country_weights, city_weights, market_weights

def company_success(status):
    if (status in ('ipo', 'acquired')):
        return True
    return False

