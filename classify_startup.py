import init_data
import company

##list of integers:*points1, *points2
def get_n_distance(*points1, *points2):
    sum = 0
    for index in range(len(points1)):
        sum += (points1[index]-points2[index])**2
    return math.sqrt(sum)

## Company:company
def get_k_neighbors(company):

## list:neighbors
def get_majority(neighbors):
    numA = 0
    numB = 0
    categoryA = ('ipo', 'aquired')
    for neighbor in neighbors:
        if neighbor.getStatus() in categoryA:
            numA += 1
        else:
            numB += 1
    if (numA > numB):
        return 1
    return 0


ref_data = init_data.parseData('data.csv')

