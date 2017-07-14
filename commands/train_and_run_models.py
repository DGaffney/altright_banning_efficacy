import os
import csv
import sys
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import tree
from sklearn import metrics
final_model = Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
    ('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
    ('clf', LogisticRegression(random_state=1))])

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

def read_csv_str(filename):
  dataset = []
  i = 0
  with open(filename, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        dataset.append(row)
  return dataset

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

def merge_conmats(conmats):
  conmat = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
  for cc in conmats:
    for key in cc.keys():
      conmat[key] += cc[key]
  return conmat

def average_conmats(conmats):
  conmat = {'tp': [], 'tn': [], 'fp': [], 'fn': []}
  for cc in conmats:
    for key in cc.keys():
      conmat[key].append(cc[key])
  return {'tp': sum(conmat['tp'])/float(len(conmats)), 'tn': sum(conmat['tn'])/float(len(conmats)), 'fp': sum(conmat['fp'])/float(len(conmats)), 'fn': sum(conmat['fn'])/float(len(conmats))}

def sensitivity(conmat):
  return float(conmat['tp'])/(conmat['tp']+conmat['fn'])

def specificity(conmat):
  return float(conmat['tn'])/(conmat['tn']+conmat['fp'])

def accuracy(conmat):
  return float(conmat['tn']+conmat['tp'])/sum(conmat.values())

filepath = os.popen('git rev-parse --show-toplevel').read().strip()
human_votes = read_csv_str(filepath+"/baumgartner_data/machine_learning_resources/"+dataset+"_human_votes.csv")
##Validation Phase
np.random.shuffle(human_votes)
comments = [r[0] for r in human_votes]
labels = [r[1] for r in human_votes]
folds = generate_folds(comments, labels, 10)
full_conmats = []
full_auc_set = []
for i in range(100):
  trial_conmats = []
  auc_set = []
  for fold in folds:
    conmat = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
    final_model.fit(fold["train_set"], fold["train_labels"])
    predicted = final_model.predict(fold["test_set"])
    auc_set.append(metrics.roc_auc_score([int(v) for v in fold["test_labels"]], predicted))
    for truth,guess in zip(fold["test_labels"], predicted):
      if float(truth) == 1 and float(guess) == 1:
        conmat['tp'] += 1
      elif float(truth) == 0 and float(guess) == 0:
        conmat['tn'] += 1
      elif float(truth) == 1 and float(guess) == 0:
        conmat['fn'] += 1
      elif float(truth) == 0 and float(guess) == 1:
        conmat['fp'] += 1
    trial_conmats.append(conmat)
  full_conmats.append(trial_conmats)
  full_auc_set.append(auc_set)

##Evaluation Phase
final_model = Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
    ('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
    ('clf', LogisticRegression(random_state=1))])
comments = [r[0] for r in human_votes]
labels = [r[1] for r in human_votes]
final_model.fit(comments, labels)
for f in os.popen('ls '+filepath+'/baumgartner_data/comments_altright').read().split("\n"):
  if f != '':
    print f
    month_data = read_csv_str(filepath+"/baumgartner_data/comments_altright/"+f)
    sentences = [r[5] for r in month_data]
    predictions = final_model.predict(sentences)
    final = []
    for row, prediction in zip(month_data, predictions):
      row.append(prediction)
      final.append(row)
    with open(filepath+"/baumgartner_data/machine_learning_results/"+dataset+"_scores_"+f, 'wb') as w:
      writer = csv.writer(w)
      writer.writerows(final)


transformed = Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
    ('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True))])

transformed.fit([r[0] for r in human_votes]).transform([r[0] for r in human_votes])[0]

CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3)).fit([r[0] for r in human_votes]).transform([r[0] for r in human_votes])
TfidfTransformer(smooth_idf=True, use_idf=True))
