import csv

#self, name, status, market, country, funding_value, funding_rounds):
def parseData_array(csvfile):
    with open(csvfile, 'rb') as data_file:
        data_reader = csv.reader(data_file, delimiter=',', quotechar='"')
        comp_arr = []
        row = 0
        for line in data_reader:
            comp_arr[row] = Company(line[0], line[3], line[1], line[4], line[2], line[7])

    return comp_arr