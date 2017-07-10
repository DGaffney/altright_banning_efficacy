import json
import pickle
import argparse
import itertools
from sklearn.neural_network import MLPClassifier
import random
import itertools
from scipy import stats
import numpy as np
import csv
from os import listdir
from os.path import isfile, join
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", help="file to learn from")
args = vars(ap.parse_args())
model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 5, 2, 5), random_state=1)
def produce_ensemble_guesses_restricted(all_guesses, fold_labels, clfs, included_clfs):
  success = 0
  count = 0.0
  conmat = {'fp': 0, 'fn': 0, 'tp': 0, 'tn': 0}
  clf_indices = []
  for clf in clfs:
    if str(clf) in included_clfs:
      clf_indices.append(1)
    else:
      clf_indices.append(0)
  sub_guesses = [g for i,g in enumerate(all_guesses) if clf_indices[i] == 1]
  aggregate_guesses = [np.mean(el) for el in np.matrix(sub_guesses).transpose().tolist()]
  for pair in np.matrix([aggregate_guesses, fold_labels]).transpose().tolist():
    count += 1
    if pair[0] > 0.5 and pair[1] == 1:
      conmat['tp'] += 1
      success += 1
    elif pair[0] > 0.5 and pair[1] == 0:
      conmat['fp'] += 1
    elif pair[0] <= 0.5 and pair[1] == 1:
      conmat['fn'] += 1
    elif pair[0] <= 0.5 and pair[1] == 0:
      conmat['tn'] += 1
      success += 1
  return conmat, success/count

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

def run_ensemble_binary(filename, models, str_columns, keys_included):
  keys, dataset, labels = dataset_array_form_from_csv(filename, str_columns, keys_included)
  folds = generate_folds(dataset, labels, fold_count=10)
  folded_results = []
  conmats = []
  guesses = []
  fold_labels = [fold["test_labels"] for fold in folds]
  for clf in models:
    #print clf
    this_conmat = {'fp': 0, 'fn': 0, 'tp': 0, 'tn': 0}
    this_guess = []
    for fold in folds:
      clf.fit(np.array(fold['train_set']), np.array(fold['train_labels']))
      predictions = list(clf.predict(fold["test_set"]))
      for prediction in predictions:
        this_guess.append(prediction)
      for pair in np.matrix([predictions, fold["test_labels"]]).transpose().tolist():
        if pair[0] >= 0.5 and pair[1] == 1:
          this_conmat['tp'] += 1
        elif pair[0] >= 0.5 and pair[1] == 0:
          this_conmat['fp'] += 1
        elif pair[0] < 0.5 and pair[1] == 1:
          this_conmat['fn'] += 1
        elif pair[0] < 0.5 and pair[1] == 0:
          this_conmat['tn'] += 1
    conmats.append(this_conmat)
    guesses.append(this_guess)
  return conmats, guesses, [item for sublist in fold_labels for item in sublist], models

def dataset_array_form_from_csv(filename, str_columns, keys_included):
  keys = []
  dataset = []
  labels = []
  bad_rows = []
  with open(filename, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = -1
    for row in reader:
      i += 1
      if keys_included and i == 0:
        keys = row
      else:
        # if '' not in row:
        record = []
        for j,val in enumerate(row):
          if j not in str_columns:
            parsed_val = None
            if val == '':
              parsed_val = None
            else:
              try:
                parsed_val = float(val)
              except ValueError:
                parsed_val = np.random.rand()
            if j == 0:
              labels.append(parsed_val)
            else:
              record.append(parsed_val)
        dataset.append(record)
  return keys, dataset, labels

def generate_folds(dataset, labels, fold_count):
	folded = []
	for i in range(fold_count):
		folded.append({'test_set': [], 'train_set': [], 'test_labels': [], 'train_labels': []})
	i = 0
	all_counts = range(fold_count)
	for i in range(len(dataset)):
		mod = i%fold_count
		folded[mod]['test_set'].append(dataset[i])
		folded[mod]['test_labels'].append(labels[i])
		for c in all_counts:
			if c != mod:
				folded[c]['train_set'].append(dataset[i])
				folded[c]['train_labels'].append(labels[i])
	return folded

all_conmats, all_guesses, fold_labels, used_models = run_ensemble_binary(args['file'], [model], [], False)
keys, dataset, labels = dataset_array_form_from_csv(args['file'], [], False)
print json.dumps({'conmat': all_conmats[0], 'predictions': all_guesses[0]})
