import re
import json
import string
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import os
import pickle
import argparse
import itertools
from sklearn.linear_model import Perceptron
from sklearn import linear_model
import random
from sklearn.neighbors import KNeighborsClassifier
import itertools
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import ensemble
from sklearn.svm import SVC
from sklearn import svm
from sklearn import linear_model
from sklearn import preprocessing
from sklearn import gaussian_process
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn import tree
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np
import csv
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import SGDClassifier
from os import listdir
from os.path import isfile, join
import numpy as np
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", help="dataset to sanitize ('background' or 'inner')")
ap.add_argument("-t", "--test", help="is test? Add in option if it's a test otherwise leave empty")
ap.add_argument("-c", "--count", help="number of workers that will be used - default is 10", type=int, default=10)
args = vars(ap.parse_args())
dataset = args["dataset"]
prefix = '' if args["test"] == None else '_test'
filepath = os.popen('git rev-parse --show-toplevel').read().strip()
path = filepath+"/baumgartner_data"+prefix+"/machine_learning_resources"
vocabulary = json.loads(open(path+"/"+dataset+'_vocabulary.json').read())
def read_csv_str(filename):
  dataset = []
  i = 0
  with open(filename, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        dataset.append(row)
  return dataset

class DenseTransformer(TransformerMixin):
  def transform(self, X, y=None, **fit_params):
    return X.todense()
  
  def fit_transform(self, X, y=None, **fit_params):
    self.fit(X, y, **fit_params)
    return self.transform(X)
  
  def fit(self, X, y=None, **fit_params):
    return self

def score_comment(comment):
  regular_expressions = ["(\(\(\(.*?\)\)\))",
  "(ethinic(|ity))",
  "(ethno(|-)state)",
  "(jew(|s))",
  "(goy(|s|im))",
  "(mexic(o|an))",
  "(rap(e|ing))",
  "(win(|ning))",
  "(iq)",
  "(jq)",
  "(joo(|s))",
  "(negro(|id|es))",
  "(caucasian(|s))",
  "(gene(|s|tics|otype|otypical))",
  "(slav(|ic))",
  "(hispanic(|s))",
  "(anti(|-)white(|ness))",
  "(radical(|ized))",
  "(gas chamber)",
  "(holocaust)",
  "(shoah(|ed))",
  "(hitler)",
  "(\/pol\/)",
  "(racial)",
  "(cancer(|ous))",
  "(cuck(|old|ed|y|ery|olding))",
  "(left(y|ies|ist))",
  "(asia(n|tic))",
  "(talmud(|ic))",
  "(trigger(y|ing|ed))",
  "(parasit(e|es|ic|ism))",
  "(immigra(nt|tion))",
  "(dindu)",
  "(dindu muffin)",
  "(dindu nuffin)",
  "(multicultural(|ism|ist))",
  "(skype)",
  "(specie(s|sism))",
  "(oven)",
  "(abo(|s))",
  "(shekel(|s))",
  "(libshit(|s))",
  "(fash(y|wave|ies))",
  "(white(|s|ness))",
  "(blm)",
  "(admixture)",
  "(alt(| |-)right)"]
  counts = []
  for regex in regular_expressions:
    counts.append(len(re.compile(regex, re.IGNORECASE).findall(comment)))
  return counts

keyword_groups = [set(el) for el in json.loads(open(filepath+"/baumgartner_data/machine_learning_resources/"+args["dataset"]+"_keyword_groups.json").read())]
researcher_labels = {}
for row in read_csv_str(filepath+"/baumgartner_data"+prefix+"/machine_learning_resources/"+args["dataset"]+"_researcher_votes.csv"):
  researcher_labels[row[0]] = float(row[1])

dataset, labels = generate_neural_net_sample_file_original(month_sets, researcher_labels)
models_used =  os.popen("ls "+path+"/"+args["dataset"]+"_neural_net_voter_*").read().split("\n")[:args["count"]]
datafiles = sorted(list(set(["missing_comments.csv"]).union(set([r.split("_")[-1] for r in os.popen("ls "+results_path).read().split("\n")]))-set(['', 'comments.csv'])))
all_data = {}
for month in datafiles:
  print month
  all_data[month] = [r[:-1] for r in read_csv_str(results_path+"/"+os.popen("ls "+results_path+" | grep "+month).read().split("\n")[0])]

model_results = {}
for i,model_used in enumerate(models_used):
  model_result = []
  print i
  for month in month_sets.keys():
    print "\t"+month
    if month == "missing_comments.csv":
      month_data = [r for r in read_csv_str(results_path+"/"+"dataset_"+args["dataset"]+"_model_"+str(i)+"_"+month) if r[3] in month_sets[month]]
    else: 
      month_data = [r for r in read_csv_str(results_path+"/"+"dataset_"+args["dataset"]+"_model_"+str(i)+"_RC_"+month) if r[3] in month_sets[month]]
    for row in month_data:
      if row[3] not in model_results.keys():
        model_results[row[3]] = []
      model_results[row[3]].append(float(row[-1]))

count_vect = CountVectorizer(decode_error="replace")
X_train_counts = count_vect.fit_transform([r[5] for r in dataset])
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tfidf = tf_transformer.fit_transform(X_train_counts).todense().tolist()
vectorizer = tf_transformer.fit_transform(X_train_counts)
pickle.dump(vectorizer.vocabulary_,open(filepath+"/baumgartner_data"+prefix+"/machine_learning_resources/inner_tfidf_model.pkl","wb"))
bot_list = ["SamMee514", "TweetPoster", "TotesMessenger", "youtubefactsbot", "autotldr", "gifv-bot", "Mentioned_Videos", "ConvertsToMetric", "OriginalPostSearcher", "sneakpeekbot", "xkcd_transcriber", "thank_mr_skeltal_bot", "HelperBot_", "image_linker_bot", "SmallSubBot", "JoeBidenBot", "autourbanbot", "PlaylisterBot", "ayylmao2dongerbot-v2", "TheWallGrows", "pm_me_your_bw_pics", "navigatorbot", "DailMail_Bot"]

for month_file in os.popen("ls "+filepath+"/baumgartner_data"+prefix+"/comments_altright").read().split("\n"):
  if month_file != '':
    print month_file
    neural_net_files = [f for f in sorted(os.popen("ls "+filepath+"/baumgartner_data"+prefix+"/machine_learning_results/").read().split("\n")) if month_file in f]
    neural_net_scores = {}
    for ii,net_file in enumerate(neural_net_files):
      for row in read_csv_str(filepath+"/baumgartner_data"+prefix+"/machine_learning_results/"+net_file):
        if ii == 0:
          neural_net_scores[row[3]] = [float(row[-1])]
        else:
          neural_net_scores[row[3]].append(float(row[-1]))
    observations = []
    for row in read_csv_str(filepath+"/baumgartner_data"+prefix+"/comments_altright/"+month_file):
      if row[2] not in bot_list:
        observations.append(row)
    
    to_score = np.array([[vocabulary.get(word, 0) for word in sentence] for sentence in keras_data_helpers.pad_sentences([keras_data_helpers.clean_str(sent).split(" ")[:max_len] for sent in [r[5].strip() for r in observations]], max_len)])
    predictions = model.predict(to_score, batch_size=10000, verbose=1)
    with open(filepath+"/baumgartner_data"+prefix+"/machine_learning_results/dataset_"+dataset+"_model_"+str(model_number)+"_"+f, "wb") as csv_file:
      writer = csv.writer(csv_file, delimiter=',')
      for observation, predicted in zip(observations, predictions):
        predicted_obs = observation
        predicted_obs.append(predicted[0])
        writer.writerow(predicted_obs)