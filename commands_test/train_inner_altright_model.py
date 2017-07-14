import sys
import re
import string
import os
import json
import pickle
import argparse
import itertools
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
import random
import itertools
from scipy import stats
import numpy as np
import csv
from os import listdir
from os.path import isfile, join
import pickle
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

def read_csv_str(filename):
  dataset = []
  i = 0
  with open(filename, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        dataset.append(row)
  return dataset

model = None
prefix = ""
dataset = ""
if sys.argv[-1] == "test":
  prefix = "_data"
if sys.argv[1] == "inner":
  model = AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None, learning_rate=0.5, n_estimators=100, random_state=None)
  dataset = "inner"
elif sys.argv[1] == "background":
  model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 5, 2, 5), random_state=1)
  dataset = "background"


dataset = "inner"
model = AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None, learning_rate=0.5, n_estimators=100, random_state=None)


filepath = os.popen('git rev-parse --show-toplevel').read().strip()
keyword_groups = [set(el) for el in json.loads(open(filepath+"/baumgartner_data/machine_learning_resources/"+dataset+"_keyword_groups.json").read())]
raw_dataset = read_csv_str(filepath+"/baumgartner_data/machine_learning_resources/"+dataset+"_dataset.csv")
human_votes = read_csv_str(filepath+"/baumgartner_data/machine_learning_resources/"+dataset+"_human_votes.csv")
csv_data = []
ii = 0
for row in raw_dataset:
  parsed = set(re.split(ur"[\u200b\s]+", re.sub('[%s]' % re.escape(string.punctuation), ' ', row[-2].lower()), flags=re.UNICODE))
  new_row = []
  for kg in keyword_groups:
    new_row.append(len(kg.intersection(parsed)))
  new_row.append(float(row[-1]))
  csv_data.append(new_row)
  ii += 1
  if ii % 1000 == 0:
    print ii

data_mat = np.matrix(csv_data)
accuracy_scores = []
sensitivity_scores = []
specificity_scores = []
for run in range(100):
  sampled_dataset = data_mat[np.random.randint(data_mat.shape[0], size=2000), :].tolist()
  features = [r[:-1] for r in sampled_dataset]
  labels = [r[-1] for r in sampled_dataset]
  folds = generate_folds(features, labels, 10)
  conmat = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
  for fold in folds:
    model.fit(fold["train_set"], fold["train_labels"])
    for i,guess in enumerate(model.predict(fold["test_set"]).tolist()):
      if guess == 1 and fold["test_labels"][i] == 1:
        conmat['tp'] += 1
      elif guess == 1 and fold["test_labels"][i] == 0:
        conmat['fp'] += 1
      elif guess == 0 and fold["test_labels"][i] == 1:
        conmat['fn'] += 1
      elif guess == 0 and fold["test_labels"][i] == 0:
        conmat['tn'] += 1



sentences = [r[-2:] for r in raw_dataset]
labels = [r[-1] for f in raw_dataset]
sent_mat = np.matrix(sentences)
sampled_csv = sent_mat[np.random.randint(sent_mat.shape[0], size=len(sentences)), :].tolist()

from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import KFold
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.svm import NuSVC
text_clf = Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
                     ('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
                     ('clf', AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None, learning_rate=0.5, n_estimators=100, random_state=None))])

folds = generate_folds([r[0] for r in sampled_csv], [r[1] for r in sampled_csv], 10)
text_clf = text_clf.fit([r[0] for r in sampled_csv], [r[1] for r in sampled_csv])
predicted = text_clf.predict([r[0] for r in sampled_csv])
labels = [r[1] for r in sampled_csv]
conmat = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
for i,guess in enumerate(predicted):
  if float(guess) == 1 and float(labels[i]) == 1:
    conmat['tp'] += 1
  elif float(guess) == 1 and float(labels[i]) == 0:
    conmat['fp'] += 1
  elif float(guess) == 0 and float(labels[i]) == 1:
    conmat['fn'] += 1
  elif float(guess) == 0 and float(labels[i]) == 0:
    conmat['tn'] += 1
conmats.append(conmat)
accuracies.append(float(conmat['tp']+conmat['tn'])/sum(conmat.values()))
sensitivities.append(float(conmat['tp'])/(conmat['tp']+conmat['fn']))
specificities.append(float(conmat['tn'])/(conmat['tn']+conmat['fp']))

pipelines = [Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
('clf', AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None, learning_rate=0.5, n_estimators=100, random_state=None))]),
Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
('clf', MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 5, 2, 5), random_state=1))]),
Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
('clf', MultinomialNB())]),
Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
('clf', SVC())]),
Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
('clf', NuSVC(kernel='rbf',nu=0.5))])]
pipelines = [  Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
  ('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
  ('clf', tree.DecisionTreeClassifier())]),
  Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
    ('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
    ('clf', tree.DecisionTreeRegressor())]),
]
conmats = []
accuracies = []
sensitivities = []
specificities = []
for fold in folds:
  pipeline.fit(fold["train_set"], fold["train_labels"])
  predicted = pipeline.predict(fold["test_set"])
  conmat = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
  for i,guess in enumerate(predicted):
    if float(guess) == 1 and float(fold["test_labels"][i]) == 1:
      conmat['tp'] += 1
    elif float(guess) == 1 and float(fold["test_labels"][i]) == 0:
      conmat['fp'] += 1
    elif float(guess) == 0 and float(fold["test_labels"][i]) == 1:
      conmat['fn'] += 1
    elif float(guess) == 0 and float(fold["test_labels"][i]) == 0:
      conmat['tn'] += 1
  conmats.append(conmat)
  accuracies.append(float(conmat['tp']+conmat['tn'])/sum((conmat.values())))
  sensitivities.append(float(conmat['tp'])/(conmat['tp']+conmat['fn']))
  specificities.append(float(conmat['tn'])/(conmat['tn']+conmat['fp']))

merge_conmats(conmats)
pipeline_results = []
sentences = human_votes
labels = [r[-1] for f in human_votes]
pipelines = [  Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
  ('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
  ('clf', tree.DecisionTreeClassifier())]),
  Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
    ('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
    ('clf', tree.DecisionTreeRegressor())]),
]
sent_mat = np.matrix(human_votes)
sampled_csv = sent_mat[np.random.randint(sent_mat.shape[0], size=2*len(sent_mat)), :].tolist()
sampled_csv = human_votes
pipeline_results = []
for pipeline in pipelines:
  conmats = []
  accuracies = []
  sensitivities = []
  specificities = []
  np.random.shuffle(sampled_csv)
  folds = generate_folds([r[0] for r in sampled_csv], [r[1] for r in sampled_csv], 10)
  for jk in range(10):
    for fold in folds:
      fold_mat = np.matrix(zip(fold["train_set"], fold["train_labels"]))
      upsampled = fold_mat[np.random.randint(fold_mat.shape[0], size=10*len(fold_mat)), :].tolist()
      pipeline.fit([r[0] for r in upsampled], [r[1] for r in upsampled])
      predicted = pipeline.predict(fold["test_set"])
      conmat = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
      for i,guess in enumerate(predicted):
        if float(guess) == 1 and float(fold["test_labels"][i]) == 1:
          conmat['tp'] += 1
        elif float(guess) == 1 and float(fold["test_labels"][i]) == 0:
          conmat['fp'] += 1
        elif float(guess) == 0 and float(fold["test_labels"][i]) == 1:
          conmat['fn'] += 1
        elif float(guess) == 0 and float(fold["test_labels"][i]) == 0:
          conmat['tn'] += 1
      conmats.append(conmat)
      accuracies.append(float(conmat['tp']+conmat['tn'])/sum((conmat.values())))
      sensitivities.append(float(conmat['tp'])/(conmat['tp']+conmat['fn']))
      specificities.append(float(conmat['tn'])/(conmat['tn']+conmat['fp']))
  pipeline_results.append([conmats, accuracies, sensitivities, specificities])

pipeline_results
accuracy(merge_conmats(pipeline_results[0][0]))
accuracy(merge_conmats(pipeline_results[1][0]))

results[dataset] = pipeline_results
thing_that_has_results = results

pipeline.fit([r[0] for r in sampled_csv], [r[1] for r in sampled_csv])
predicted = pipeline.predict([r[0] for r in sampled_csv])

/media/dgaff/backup/Code/altright_banning_efficacy
def merge_conmats(conmats):
  conmat = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
  for cc in conmats:
    for key in cc.keys():
      conmat[key] += cc[key]
  return conmat

pipeline = Pipeline([('vect', CountVectorizer(stop_words='english', ngram_range=(1,3))),
('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
('clf', MultinomialNB())])
full_conmats = []
full_accuracies = []
full_sensitivities = []
full_specificities = []
for i in range(100):
  np.random.shuffle(sampled_csv)
  folds = generate_folds([r[0] for r in sampled_csv], [r[1] for r in sampled_csv], 10)
  tree.DecisionTreeRegressor()
  conmats = []
  accuracies = []
  sensitivities = []
  specificities = []
  for fold in folds:
    pipeline.fit(fold["train_set"], fold["train_labels"])
    predicted = pipeline.predict(fold["test_set"])
    conmat = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
    for i,guess in enumerate(predicted):
      if float(guess) == 1 and float(fold["test_labels"][i]) == 1:
        conmat['tp'] += 1
      elif float(guess) == 1 and float(fold["test_labels"][i]) == 0:
        conmat['fp'] += 1
      elif float(guess) == 0 and float(fold["test_labels"][i]) == 1:
        conmat['fn'] += 1
      elif float(guess) == 0 and float(fold["test_labels"][i]) == 0:
        conmat['tn'] += 1
    conmats.append(conmat)
    accuracies.append(float(conmat['tp']+conmat['tn'])/sum((conmat.values())))
    sensitivities.append(float(conmat['tp'])/(conmat['tp']+conmat['fn']))
    specificities.append(float(conmat['tn'])/(conmat['tn']+conmat['fp']))
  full_conmats.append(merge_conmats(conmats))
  full_accuracies.append(sum(accuracies)/10)
  full_sensitivities.append(sum(sensitivities)/10)
  full_specificities.append(sum(specificities)/10)

stripped_results = [full_conmats, full_accuracies, full_sensitivities, full_specificities]


specific_model = Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
('clf', AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None, learning_rate=0.5, n_estimators=100, random_state=None))])

sensitive_model = Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
('clf', NuSVC(kernel='rbf',nu=0.5))])

specific_model.fit([r[0] for r in sampled_csv], [r[1] for r in sampled_csv])
sensitive_model.fit([r[0] for r in sampled_csv], [r[1] for r in sampled_csv])
specific_predicted = specific_model.predict([r[0] for r in sampled_csv])
sensitive_predicted = sensitive_model.predict([r[0] for r in sampled_csv])
total = 0
conmat = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
for k,specific_guess in enumerate(specific_predicted):
  ultimate_vote = None
  if float(specific_guess) == 0:
    ultimate_vote = 0
  elif float(sensitive_predicted[k]) == 1:
    ultimate_vote = 1
  else:
    ultimate_vote = 0
  if ultimate_vote == float(sampled_csv[k][1]):
    total += 1
  if ultimate_vote == 1 and float(sampled_csv[k][1]) == 1:
    conmat['tp'] += 1
  elif ultimate_vote == 1 and float(sampled_csv[k][1]) == 0:
    conmat['fp'] += 1
  elif ultimate_vote == 0 and float(sampled_csv[k][1]) == 0:
    conmat['tn'] += 1
  elif ultimate_vote == 0 and float(sampled_csv[k][1]) == 1:
    conmat['fn'] += 1

float(total)/len(specific_predicted)
all_conmats = []
for i in range(100):
  conmats = []
  np.random.shuffle(sampled_csv)
  folds = generate_folds([r[0] for r in sampled_csv], [r[1] for r in sampled_csv], 10)
  for fold in folds:  
    specific_model.fit(fold["train_set"], fold["train_labels"])
    sensitive_model.fit(fold["train_set"], fold["train_labels"])
    specific_predicted = specific_model.predict(fold["test_set"])
    sensitive_predicted = sensitive_model.predict(fold["test_set"])
    conmat = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
    for k,specific_guess in enumerate(specific_predicted):
      ultimate_vote = None
      if float(specific_guess) == 0:
        ultimate_vote = 0
      elif float(sensitive_predicted[k]) == 1:
        ultimate_vote = 1
      else:
        ultimate_vote = 0
      if ultimate_vote == float(fold["test_labels"][k]):
        total += 1
      if ultimate_vote == 1 and float(fold["test_labels"][k]) == 1:
        conmat['tp'] += 1
      elif ultimate_vote == 1 and float(fold["test_labels"][k]) == 0:
        conmat['fp'] += 1
      elif ultimate_vote == 0 and float(fold["test_labels"][k]) == 0:
        conmat['tn'] += 1
      elif ultimate_vote == 0 and float(fold["test_labels"][k]) == 1:
        conmat['fn'] += 1
        print k
    conmats.append(conmat)
  all_conmats.append(conmats)




csv_data = []
labels = []
ii = 0
for row in human_votes:
  parsed = set(re.split(ur"[\u200b\s]+", re.sub('[%s]' % re.escape(string.punctuation), ' ', row[0].lower()), flags=re.UNICODE))
  labels.append(row[1])
  new_row = []
  for kg in keyword_groups:
    new_row.append(len(kg.intersection(parsed)))
  new_row.append(len(row[0]))
  csv_data.append(new_row)
  ii += 1
  if ii % 1000 == 0:
    print ii

transformed = Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
    ('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True))])

transformed_data = [r.toarray().tolist()[0] for r in transformed.fit([r[0] for r in human_votes]).transform([r[0] for r in human_votes])]
merged = []
for t,cc in zip(transformed_data, csv_data):
  merged.append([item for sublist in [t,cc] for item in sublist])

trim_results = sklearn.feature_selection.chi2(transformed_data, labels)
from sklearn import preprocessing
folds = generate_folds([r[0] for r in human_votes], [int(r[1]) for r in human_votes], 10)
accuracies = []
for clf in models:
  trial_conmats = []
  auc_set = []
  for fold in folds:
    conmat = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
    clf.fit(fold["train_set"], [int(r) for r in fold["train_labels"]])
    predicted = clf.predict(fold["test_set"])
    auc_set.append(metrics.roc_auc_score([int(v) for v in fold["test_labels"]], predicted))
    ii = 0
    for truth,guess in zip([int(r) for r in fold["test_labels"]], predicted):
      if fold["test_set"][ii][-1] > 100:
        if float(truth) == 1 and float(guess) == 1:
          conmat['tp'] += 1
        elif float(truth) == 0 and float(guess) == 0:
          conmat['tn'] += 1
        elif float(truth) == 1 and float(guess) == 0:
          conmat['fn'] += 1
        elif float(truth) == 0 and float(guess) == 1:
          conmat['fp'] += 1
      ii += 1
    trial_conmats.append(conmat)
  accuracies.append(accuracy(merge_conmats(trial_conmats)))
