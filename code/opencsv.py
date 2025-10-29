import os
#import numpy
import csv
from pathlib import Path
#import re
# todo:
# test code         add batching
dataset_folder = os.path.join(Path(__file__).resolve().parent.parent, 'data')
path = os.path.join(dataset_folder, '1v1replays.csv')
# now take the ids and make a dataset with 10 batches to get a array of 10*100
# format of the ids: UUID
def read_ids(path, delimiter=','):
    ids = []
    with open(path, newline='',encoding='utf-8' ) as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            for cell in row:
                cell = cell.strip()
                if cell:
                    ids.append(cell)
    return ids


if __name__ == "__main__":
    ids = read_ids(path)
    print("found", len(ids), "IDs. First 10:", ids[:10])
