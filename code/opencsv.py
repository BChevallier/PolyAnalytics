import os
#import numpy
import csv
#import re
# todo:
# test code         add batching
dataset_folder = os.path.join(os.getcwd(), 'data')
path = os.path.join(dataset_folder, '1v1replays.csv')

# now take the ids and make a dataset with 10 batches to get a array of 10*100
# format of the ids: UUID
def read_ids(path, delimiter=','):
    ids = []
    with open(path, newline=' ',encoding='utf-8' ) as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            for cell in row:
                cell = cell.strip
                ids.append(cell)
    return ids


#test:
print(read_ids(path))

