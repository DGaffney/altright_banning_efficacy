import csv
import json
import os
import argparse
import numpy as np
import h5py
import keras_data_helpers
from keras_w2v import train_word2vec
from keras.models import load_model
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Input, MaxPooling1D, Convolution1D, Embedding
from keras.layers.merge import Concatenate
from keras.preprocessing import sequence
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

def load_data(path, dataset):
  x, y, vocabulary, vocabulary_inv_list = keras_data_helpers.load_data(path, dataset)
  vocabulary_inv = {key: value for key, value in enumerate(vocabulary_inv_list)}
  y = y.argmax(axis=1)
  # Shuffle data
  shuffle_indices = np.random.permutation(np.arange(len(y)))
  x = x[shuffle_indices]
  y = y[shuffle_indices]
  return x, y, vocabulary, vocabulary_inv

x, y, vocabulary, vocabulary_inv = load_data(path, dataset)
max_len = sorted([len(r) for r in x.tolist()])[-1]
models = []
for model_file in sorted(os.popen("ls "+path+"/"+dataset+"_neural_net_voter_*").read().split("\n"))[1:args["count"]+1]:
  if model_file != '':
    models.append(load_model(model_file))

file_scores = {}
#Originally coded in https://docs.google.com/spreadsheets/d/1lMgnAvokvdRw1OTRqrsw-jpcMc8hCzBm_pcxf-235ks/edit#gid=0
bot_list = ["SamMee514", "TweetPoster", "TotesMessenger", "youtubefactsbot", "autotldr", "gifv-bot", "Mentioned_Videos", "ConvertsToMetric", "OriginalPostSearcher", "sneakpeekbot", "xkcd_transcriber", "thank_mr_skeltal_bot", "HelperBot_", "image_linker_bot", "SmallSubBot", "JoeBidenBot", "autourbanbot", "PlaylisterBot", "ayylmao2dongerbot-v2", "TheWallGrows", "pm_me_your_bw_pics", "navigatorbot", "DailMail_Bot"]

for f in os.popen("ls "+filepath+"/baumgartner_data"+prefix+"/comments_altright").read().split("\n"):
  if f != '':
    print f
    for model_number,model in enumerate(models):
      observations = []
      for row in read_csv_str(filepath+"/baumgartner_data"+prefix+"/comments_altright/"+f):
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

observations = []
for row in read_csv_str("/media/dgaff/backup/Code/altright_banning_efficacy/baumgartner_data/machine_learning_resources/inner_human_votes_nnet_test.csv"):
  if row[1] not in bot_list:
    observations.append(row)

to_score = np.array([[vocabulary.get(word, 0) for word in sentence] for sentence in keras_data_helpers.pad_sentences([keras_data_helpers.clean_str(sent).split(" ")[:max_len] for sent in [r[5].strip() for r in observations]], max_len)])
predictions = []
for model in models:
  try:
    predictions.append([el[0] for el in model.predict(to_score, batch_size=10000, verbose=1).tolist()])
  except:
    print "old model"
np.matrix([[el[0] for el in x.tolist()] for x in predictions]).transpose()