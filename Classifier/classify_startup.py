import sys
import datetime
import os.path
import init_data as init
import cPickle
import argparse
from math import sqrt
from operator import itemgetter
from Company import Company


## list of integers:points1, points2
## Returns integer distance
# TODO : abs(X-Y) / X+Y
# UNLESS X+Y = 0.
# Gives you the difference in % of the total of both
DATE_SCALE = 365*5
def get_n_distance(points1, points2):
    sum = 0.0
    for index in range(len(points1)):
        diff = 1
        if points1[index] is not None and points2[index] is not None:
            diff = abs(points1[index] - points2[index])

            if isinstance(points1[index], datetime.date):
                scale = 1
                if diff.days < DATE_SCALE:
                    scale = float(diff.days/DATE_SCALE)
                sum += scale
            else:
                try:
                    sum += float(diff/(points1[index] + points2[index]))
                except ZeroDivisionError:
                    pass
        else:
            sum += diff

        # Both X and Y should be positive. Only 0 would be X = 0 and Y = 0


    return sum

## Company:company List:data Dict:country_weights, market_weights
## Returns: list of neighbors
def get_k_neighbors(company, k, data, country_weights, city_weights, market_weights):
    k_neighbours = []
    for ref_company in data:

        # Gets the distance based on anything numerical
        distance = get_n_distance(company.get_numerical_points(), \
        ref_company.get_numerical_points())

        if(company.country == ref_company.country):
            distance *= country_weights[ref_company.country]

        if(company.city == ref_company.city):
            distance *= city_weights[ref_company.city]

        if(company.market == ref_company.market):
            distance *= market_weights[ref_company.market]

        if len(k_neighbours) >= k:
            if (distance < k_neighbours[k-1][0]):
                k_neighbours[k-1] = (distance,ref_company)
                k_neighbours.sort(key=itemgetter(0))
        else:
            k_neighbours.append((distance,ref_company))

    return k_neighbours

## list:neighbors
## Returns: 1 == Successful, 0 == Failure, -1 == Uncertain
def success_rate(neighbors):
    num_successful = 0
    num_failures = 0
    for neighbor in neighbors:
        if neighbor[1].successful:
            num_successful += 1
        else:
            num_failures += 1
    diff = num_successful - num_failures
    # Has to have a diff
    sureness = float(num_successful/len(neighbors))

    # At least 65% of results one way
    if sureness < 0.35 or sureness > 0.65:
        if diff > 0:
            return 1
        else:
            return 0

    # Return unsure doesn't fall into the acceptable results range
    return -1

## -
## Returns: all dictionaries for classification and verification.
def initialize():
    print "Initializing Data.."
    ref_data, test_data, country_weights, city_weights, market_weights = [], [], {}, {}, {}
    ref_data, test_data, country_weights, city_weights, market_weights = init.parseData('analytics_2')

    data_structs = (country_weights, city_weights, market_weights)
    iter_data = (ref_data,test_data)

    names = ('country_weights', 'city_weights', 'market_weights')
    iter_names = ('ref_data','test_data')

    print "Pickling Data.."
    if not os.path.exists('.pickle/'):
        print "No Pickle directory found.."
        print "Creating one at {0}/.pickle".format(os.getcwd())
        os.makedirs('.pickle/')

    for i in range(len(names)):
        with open('.pickle/.{0}.pickle'.format(names[i]), 'wb') as f:
            cPickle.dump(data_structs[i], f, protocol=cPickle.HIGHEST_PROTOCOL)

    for i in range(len(iter_names)):
        with open('.pickle/.{0}.pickle'.format(iter_names[i]), 'wb') as f:
            for data in iter_data[i]:
                cPickle.dump(data,f,protocol=cPickle.HIGHEST_PROTOCOL)

    return 1

## -
## Returns: True == initialized data, False == uninitialized data
def is_initialized():
    names = ('ref_data', 'test_data', 'country_weights', 'city_weights', 'market_weights')
    for name in names:
      if not os.path.exists(".pickle/.{0}.pickle".format(name)):
          return False
    return True

## k: integer
## Returns: console print out of test results on k neighbors.
def test(k=9):
    print "Starting Test.."
    initialize()

    test_data = load_in('.pickle/.test_data.pickle')

    correct = 0
    wrong = 0
    total_tested = 0
    # PRINTING PARAMS for prettiness
    to = 100
    digits = len(str(to - 1))
    delete = "\b" * (digits + 1 + len("Correct: {3}  Wrong: {4}"))

    for company in test_data:
        if classify(company, k) == company.successful:
            correct += 1
        else:
            wrong += 1

        total_tested += 1
        print "Accuracy: {0}%  Correct: {1}  Wrong: {2}".format(float(correct)/float(wrong+correct) * 100, correct,wrong)
        #sys.stdout.write("{0}Correct: {1}  Wrong: {2}".format(delete, correct, wrong))
        #sys.stdout.flush()

    print "Tested {0} entries with k={2}:".format(total_to_test, k)
    if (wrong > 0):
        print "\n{0}% accuracy for {1} neighbors.".format(float(correct)/float(total_to_test) * 100, k)
    else:
        print "\n100% accuracy for {0} neighbors.".format(k)

# Classifies your startup
# Returns: 1==Successful 0==Failure -1==Uncertain -2==Error
def classify(company, k = 9):
    #Check that the Data is initialized
    #TODO: CHANGE THIS SO INPUT MATCHES ACTUAL COMPANY FORMAT

    ref_data, country_weights, city_weights, market_weights = grab_files()

    print("Crunching numbers. . .")
    comparable_companies = get_k_neighbors(company,k,ref_data,country_weights,\
    city_weights,market_weights)
    for data in comparable_companies:
        company = data[1]
        print(company.name,company.status,company.market,company.country,\
        company.city,company.founded,company.relationships, company.invest_rounds,\
        company.first_invest,company.last_invest,company.funding_rounds,\
        company.funding_total,company.first_funding,company.last_funding,
        company.successful)
    return success_rate(comparable_companies)

def grab_files():
    print("Opening pickles. . .")

    ref_data = load_in('.pickle/.ref_data.pickle')

    with open('.pickle/.country_weights.pickle', 'rb') as f:
        country_weights = cPickle.load(f)
    with open('.pickle/.city_weights.pickle', 'rb') as f:
        city_weights = cPickle.load(f)
    with open('.pickle/.market_weights.pickle', 'rb') as f:
        market_weights = cPickle.load(f)
    return ref_data, country_weights, city_weights, market_weights

# Generator to iter through pickle
def load_in(f_name):
    with open(f_name, "rb") as f:
        while True:
            try:
                yield cPickle.load(f)
            except EOFError:
                break
## MAIN
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-test', action="store_true")
    parser.add_argument('-clean', action='store_true')
    parser.add_argument('-n', type=str)
    parser.add_argument('-s', type=str)
    parser.add_argument('-m', type=str)
    parser.add_argument('-co', type=str)
    parser.add_argument('-ci', type=str)
    parser.add_argument('-fo', type=str)
    parser.add_argument('-r', type=int)
    parser.add_argument('-ir', type=str)
    parser.add_argument('-fi', type=str)
    parser.add_argument('-li', type=str)
    parser.add_argument('-fr', type=int)
    parser.add_argument('-ft', type=float)
    parser.add_argument('-ff', type=str)
    parser.add_argument('-lf', type=str)
    parser.add_argument('-k', type=int, default=9)
    args = parser.parse_args()

    if args.test:
        test(args.k)
    else:
        if (not is_initialized()) or args.clean:
            initialize()

        date_inputs = [args.fi,args.li,args.ff,args.lf,args.fo]
        i = 0
        while i <  len(date_inputs):
            if date_inputs[i]:
                date_inputs[i] = datetime.date(int(date_inputs[i][:4]), \
                int(date_inputs[i][5:7]), int(date_inputs[i][8:10]))
            i += 1

        company = Company(args.n,args.s,args.m,args.co,args.ci, date_inputs[4], \
        args.r, args.ir, date_inputs[0], date_inputs[1], \
        args.fr, args.ft, date_inputs[2], date_inputs[3])

        print(classify(company,args.k))

if __name__ == '__main__':
    main()

# if (len(sys.argv) == 2):
#     if sys.argv[1] == 'test':
#         test()
# elif (len(sys.argv) == 3):
#     if sys.argv[1] == 'test':
#         test(k=int(sys.argv[2]))
# elif (len(sys.argv) == 10):
#     print(classify(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9]))
# elif (len(sys.argv) == 11):
#     print(classify(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], k=int(sys.argv[10])))
# else:
#    print("ERROR: invalid argument(s).")
