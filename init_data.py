import csv

with open('data.csv', 'rb') as data_file:
    data_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    comp_arr = []
    for row in spamreader:

