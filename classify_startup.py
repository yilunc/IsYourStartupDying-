import init_data as init
from Company import Company
from math import sqrt

##list of integers:points1, points2
def get_n_distance(points1, points2):
    sum = 0
    for index in range(len(points1)):
        sum += (points1[index] - points2[index]) ** 2
    return sqrt(sum)

## Company:company List:data Dict:country_weights, market_weights
def get_k_neighbors(company, k, data, country_weights, city_weights, market_weights):
    print("    Getting " + str(k) + " nearest neighbors...")
    distances = {}
    for ref_company in data:
        distance = get_n_distance((company.getFunding_value(), company.getFunding_rounds()),(ref_company.getFunding_value(), ref_company.getFunding_rounds()))

        if(company.getCountry() == ref_company.getCountry()):
            distance /= country_weights[company.getCountry()]
        else:
            distance *= country_weights[company.getCountry()]


        if(company.getCity() == ref_company.getCity()):
            distance /= city_weights[company.getCity()]
        else:
            distance *= city_weights[company.getCity()]


        if(company.getMarket() == ref_company.getMarket()):
            distance /= market_weights[company.getMarket()]
        else:
            distance *= market_weights[company.getMarket()]


        if (distance in distances):
            distances[distance].append(ref_company)
        else:
            distances[distance] = [ref_company]

    sorted_keys = distances.keys()
    sorted_keys.sort()

    nearest_neighbors = []

    index = 0
    while (index < k):
        num_added = 0
        for company in distances[sorted_keys[index]]:
            nearest_neighbors.append(company)
            num_added += 1
            if(num_added + index >= k):
                break
        index += num_added

    for neighbour in nearest_neighbors:
        print
        print(neighbour.getName())
        print(neighbour.getFunding_value())
        print(neighbour.getFunding_rounds())
        print(neighbour.getStatus())
        print
    return nearest_neighbors

## list:neighbors
## 1 == Successful, 0 == Failure, -1 == Uncertain
def get_majority(neighbors):
    print("    Getting majority")
    numA = 0
    numB = 0
    categoryA = ('ipo', 'acquired', 'operating')

    for neighbor in neighbors:
        if neighbor.getStatus() in categoryA:
            numA += 1
        else:
            numB += 1

    diff = numA - numB

    if (abs(diff) < len(neighbors)*0.05):
        return -1
    elif (diff > 0):
        return 1
    return 0


ref_data, country_weights, city_weights, market_weights = init.parseData('data.csv')

## main
print([c.getName() for c in ref_data[:10]])
print(country_weights.values()[:10], country_weights['USA'])
print(market_weights.values()[:10])
print(get_majority(get_k_neighbors(Company("hello", "" , "Curated Web", "USA", "San Francisco", 120, 1, 1), 3, ref_data, country_weights, city_weights, market_weights)))
