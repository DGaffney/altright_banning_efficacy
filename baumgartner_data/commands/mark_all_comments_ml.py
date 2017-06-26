import json
import pickle
import csv
import argparse
from os import listdir
from os.path import isfile, join
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", help="file to learn from")
ap.add_argument("-m", "--model", help="model to be used")
args = vars(ap.parse_args())
model = pickle.loads(open(args['model']).read())
def read_csv(filename):
  dataset = []
  i = 0
  with open(filename, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        if i != 0:  
          dataset.append([float(el) for el in row])
        i += 1
  return dataset

dataset = read_csv(args['file'])
print json.dumps(model.predict(dataset).tolist())