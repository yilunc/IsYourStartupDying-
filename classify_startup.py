import init_data as init
from company import Company
from math import sqrt

##list of integers:points1, points2
def get_n_distance(points1, points2):
    sum = 0
    for index in range(len(points1)):
        sum += (points1[index] - points2[index]) ** 2
    return sqrt(sum)

## Company:company List:data Dict:country_weights, market_weights
def get_k_neighbors(company, k, data, country_weights, market_weights):
    print("    Getting " + str(k) + " nearest neighbors...")
    distances = {}
    for ref_company in data:
        distance = get_n_distance((company.getFunding_value(), company.getFunding_rounds()),(ref_company.getFunding_value(), ref_company.getFunding_rounds()))
        distance *= country_weights[company.getCountry()]
        distance *= market_weights[company.getMarket()]

        if (distance in distances):
            distances[distance].append(ref_company)
        else:
            distances[distance] = [ref_company]

    ##TODO find python sorting alg
    sorted_keys = distances.keys()
    sorted_keys.sort()

    nearest_neighbors = []
    for i in range(k):
        for company in distances[sorted_keys[i]]:
            nearest_neighbors.append(company)

    return nearest_neighbors

## list:neighbors
## 1 == Successful, 0 == Failure, -1 == Uncertain
def get_majority(neighbors):
    print("    Getting majority")
    numA = 0
    numB = 0
    categoryA = ('ipo', 'aquired')

    for neighbor in neighbors:
        if neighbor.getStatus() in categoryA:
            numA += 1
        else:
            numB += 1

    diff = numA - numB

    if (abs(diff) < 3):
        return -1
    elif (diff > 0):
        return 1
    return 0


ref_data, country_weights, market_weights = init.parseData('data.csv')

## main
print([c.getName() for c in ref_data[:10]])
print(country_weights.values()[:10])
print(market_weights.values()[:10])
print()
print(get_majority(get_k_neighbors(Company("hello", "" , "Crowdsourcing", "USA", 12341212212123, 1), 11, ref_data, country_weights, market_weights)))
