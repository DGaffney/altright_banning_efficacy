import string
import re
import json
import pickle
import csv
import argparse
import os
from os import listdir
from os.path import isfile, join
filepath = os.popen('git rev-parse --show-toplevel').read().strip()
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", help="file to learn from")
args = vars(ap.parse_args())
model = pickle.loads(open(filepath+"/baumgartner_data/commands/ml_model_altright.pkl").read())
def read_csv(filename):
  dataset = []
  i = 0
  with open(filename, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        dataset.append([float(el) for el in row])
  return dataset

def read_csv_str(filename):
  dataset = []
  i = 0
  with open(filename, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        dataset.append(row)
  return dataset

raw_dataset = read_csv_str(filepath+"/baumgartner_data/comments_altright/"+args['file'])
keyword_groups = [set(el) for el in json.loads(open(filepath+"/baumgartner_data/machine_learning/keyword_groups.json").read())]
csv_data = []
ii = 0
for row in raw_dataset:
  parsed = set(re.split(ur"[\u200b\s]+", re.sub('[%s]' % re.escape(string.punctuation), ' ', row[-1].lower()), flags=re.UNICODE))
  new_row = []
  for kg in keyword_groups:
    new_row.append(len(kg.intersection(parsed)))
  csv_data.append(new_row)
  ii += 1
  if ii % 1000 == 0:
    print ii

with open(filepath+"/baumgartner_data/comments_altright_ml_transformed/"+args['file'], 'wb') as f:
  writer = csv.writer(f)
  writer.writerows(csv_data)

predictions = model.predict(csv_data).tolist()
raw_merged = []
for i,row in enumerate(raw_dataset):
  row.append(predictions[i])
  raw_merged.append(row)

with open(filepath+"/baumgartner_data/comments_altright_ml_predicted/"+args['file'], 'wb') as f:
  writer = csv.writer(f)
  writer.writerows(raw_merged)
