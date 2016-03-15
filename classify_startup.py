import sys
import datetime
import os.path
import init_data as init
from Company import Company
from math import sqrt
import pickle

## list of integers:points1, points2
## Returns integer distance
def get_n_distance(points1, points2):
    sum = 0.0
    for index in range(len(points1)):
        sum += float(points1[index] - points2[index]) ** 2
    return float(sqrt(sum))

## Company:company List:data Dict:country_weights, market_weights
## Returns: list of neighbors
def get_k_neighbors(company, k, data, country_weights, city_weights, market_weights):
    distances = {}
    for ref_company in data:
        distance = get_n_distance((company.getFunding_value(), company.getFunding_rounds(), company.getFunding_per_date()),
                                  (ref_company.getFunding_value(), ref_company.getFunding_rounds(), ref_company.getFunding_per_date()))

        if (company.getCountry() in country_weights):
            if(company.getCountry() == ref_company.getCountry()):
                distance /= country_weights[company.getCountry()]
            else:
                distance *= country_weights[company.getCountry()]

        if (company.getCity() in city_weights):
            if(company.getCity() == ref_company.getCity()):
                distance /= city_weights[company.getCity()]
            else:
                distance *= city_weights[company.getCity()]

        if (company.getMarket() in market_weights):
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
            if(index + num_added >= k):
                break
        index += num_added
    return nearest_neighbors

## list:neighbors
## Returns: 1 == Successful, 0 == Failure, -1 == Uncertain
def get_majority(neighbors):
    numA = 0
    numB = 0
    for neighbor in neighbors:
        if company_status(neighbor):
            numA += 1
        else:
            numB += 1
    diff = numA - numB
    if (abs(diff) < len(neighbors)*0.05):
        return -1
    elif (diff > 0):
        return 1
    return 0

## Company:company
## Returns: True == Successful False == Failure
def company_status(company):
    return company.getStatus() in ('ipo', 'acquired') or company.getFunding_per_date() > init.MONEYTHRESHOLD

def initialize():
    print "Initializing Data.."
    ref_data, train_data, country_weights, city_weights, market_weights = [], [], {}, {}, {}
    ref_data, train_data, country_weights, city_weights, market_weights = init.parseData('data.csv')
    data_structs = (ref_data, train_data, country_weights, city_weights, market_weights)
    names = ('ref_data', 'train_data', 'country_weights', 'city_weights', 'market_weights')
    print "Pickling Data.."
    if not os.path.exists('.pickle/'):
        print "No Pickle directory found.."
        print "Creating one at {0}/.pickle".format(os.getcwd())
        os.makedirs('.pickle/')
    for i in range(len(names)):
        with open('.pickle/.{0}.pickle'.format(names[i]), 'wb') as f:
            pickle.dump(data_structs[i], f)
    return ref_data, train_data, country_weights, city_weights, market_weights

def is_initialized():
    names = ('ref_data', 'train_data', 'country_weights', 'city_weights', 'market_weights')
    for name in names:
      if not os.path.exists(".pickle/.{0}.pickle".format(name)):
          return False
    return True

def test(k=9):
    print "Starting Test.."
    ref_data, train_data, country_weights, city_weights, market_weights = initialize()
    correct = 0
    wrong = 0
    total_to_test = len(train_data)
    test_num = 0
    # PRINTING PARAMS for prettiness
    to = 100
    digits = len(str(to - 1))
    delete = "\b" * (digits + 1 + len("Progress: %   Correct: {3}  Wrong: {4}"))
    print "Running test on {0} entries with k={1}:".format(total_to_test, k)
    for company in train_data:
        if (get_majority(get_k_neighbors(company, k, ref_data, country_weights, city_weights, market_weights)) == company_status(company)):
            correct += 1
        else:
            wrong += 1
        test_num += 1
        sys.stdout.write("{0}Progress: {1:{2}}%   Correct: {3}  Wrong: {4}".format(delete, int((float(test_num)/float(total_to_test)) * 100), digits, correct, wrong))
        sys.stdout.flush()
    if (wrong > 0):
        print "\n{0}% accuracy for {1} neighbors.".format(float(correct)/float(total_to_test) * 100, k)
    else:
        print "\n100% accuracy for {1} neighbors.".format(k)

# Classifies your startup
# Returns: 1==Successful 0==Failure -1==Uncertain -2==Error
def classify(name, status, market, country, city, funding_value, funding_rounds, first_round_date, last_round_date, k=9):
    #Check that the Data is initialized
    if not is_initialized():
        initialize()
    #Initialize the company
    d1 = datetime.date(int(first_round_date[:4]), int(first_round_date[5:7]), int(first_round_date[8:10]))
    d2 = datetime.date(int(last_round_date[:4]), int(last_round_date[5:7]), int(last_round_date[8:10]))
    delta = (d2 - d1).days
    delta = 1 if (delta == 0) else abs(delta)
    money_delta = int(funding_value)/(float(delta) / 365.0)
    company = Company(name, status, market, country, city, int(funding_value), int(funding_rounds), money_delta)
    with open('.pickle/.ref_data.pickle', 'rb') as f:
        ref_data = pickle.load(f)
    with open('.pickle/.train_data.pickle', 'rb') as f:
        train_data = pickle.load(f)
    with open('.pickle/.country_weights.pickle', 'rb') as f:
        country_weights = pickle.load(f)
    with open('.pickle/.city_weights.pickle', 'rb') as f:
        city_weights = pickle.load(f)
    with open('.pickle/.market_weights.pickle', 'rb') as f:
        market_weights = pickle.load(f)
    return get_majority(get_k_neighbors(company, k, ref_data, country_weights, city_weights, market_weights))


## MAIN
if (len(sys.argv) == 2):
    if sys.argv[1] == 'test':
        test()
elif (len(sys.argv) == 3):
    if sys.argv[1] == 'test':
        test(k=int(sys.argv[2]))
elif (len(sys.argv) == 10):
    print(classify(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9]))
elif (len(sys.argv) == 11):
    print(classify(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], k=int(sys.argv[10])))
else:
   print("ERROR: invalid argument(s).")


