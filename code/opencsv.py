import os
#import numpy
import csv
from pathlib import Path
import re
import pandas as pd
import numpy as np



dataset_folder = os.path.join(Path(__file__).resolve().parent.parent, 'data')
path = os.path.join(dataset_folder, '1v1replays.csv')

# now take the ids and make a dataset with 10 batches to get a array of 10*100
# format of the ids: UUID
def read_ids(path: path, delimiter=',') -> list[str]:
    ids = []
    with open(path, newline='',encoding='utf-8' ) as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            for cell in row:
                cell = cell.strip()
                if cell:
                    ids.append(cell)
    return ids
#change from 'list' of ids dataset with following batching:
# 10 rows x 100 column
def batch_ids():
    ids = read_ids(path)

    arr = np.array(ids, dtype=object).reshape((1000, 10))
    df = pd.DataFrame(arr)
    df.to_csv('out.csv', index=False, header=False) 

if __name__ == "__main__":
    ids = read_ids(path)
    print("found", len(ids), "IDs. First 10:", ids[:10])
