import os
import csv
import sys
import re
import argparse
import keras_data_helpers
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", help="dataset to sanitize ('background' or 'inner')")
ap.add_argument("-t", "--test", help="is test? Add in option if it's a test otherwise leave empty")
args = vars(ap.parse_args())

def read_csv_str(filename):
  dataset = []
  i = 0
  with open(filename, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        dataset.append(row)
  return dataset

dataset = args["dataset"]
prefix = '' if args["test"] == None else '_test'
filepath = os.popen('git rev-parse --show-toplevel').read().strip()
human_votes = read_csv_str(filepath+"/baumgartner_data"+prefix+"/machine_learning_resources/"+dataset+"_human_votes_nnet.csv")
pos_votes = [[keras_data_helpers.clean_str(r[8]), r[-1]] for r in human_votes[1:] if float(r[-1]) == 1]
neg_votes = [[keras_data_helpers.clean_str(r[8]), r[-1]] for r in human_votes[1:] if float(r[-1]) == 0]

with open(filepath+"/baumgartner_data"+prefix+"/machine_learning_resources/altright-"+dataset+".pos", 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(pos_votes)

with open(filepath+"/baumgartner_data"+prefix+"/machine_learning_resources/altright-"+dataset+".neg", 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(neg_votes)
