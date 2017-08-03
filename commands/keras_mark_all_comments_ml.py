from nltk.stem import PorterStemmer
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
args['dataset'] = 'inner'
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
for row in read_csv_str("/media/dgaff/backup/Code/altright_banning_efficacy/baumgartner_data/machine_learning_resources/inner_human_votes_testing.csv"):
  if row[2] not in bot_list:
    observations.append(row)

cleaned_sents = [str.join(" ", [PorterStemmer().stem(keras_data_helpers.stem_word(word)) for word in keras_data_helpers.clean_str(r[5]).split(" ")]) for r in observations]
to_score = np.array([[vocabulary.get(word, 0) for word in sentence] for sentence in keras_data_helpers.pad_sentences([keras_data_helpers.clean_str(sent).split(" ")[:max_len] for sent in cleaned_sents], max_len)])
predictions = []
for model in models:
  try:
    predictions.append([el[0] for el in model.predict(to_score, batch_size=10, verbose=1).tolist()])
  except:
    print "old model"

guesses = [np.mean(r) for r in np.matrix(predictions[:2]).transpose()]
conmats = []
for guesses in predictions:
  conmat = {'fp': 0, 'fn': 0, 'tp': 0, 'tn': 0}
  for i,obs in enumerate(observations):
    if float(obs[-2]) < 0.5 and guesses[i] < 0.5:
      conmat['tn'] += 1
    elif float(obs[-2]) < 0.5 and guesses[i] > 0.5:
      conmat['fp'] += 1
    elif float(obs[-2]) > 0.5 and guesses[i] > 0.5:
      conmat['tp'] += 1
    elif float(obs[-2]) > 0.5 and guesses[i] < 0.5:
      conmat['fn'] += 1
  conmats.append(conmat)

irr_conmat = {'fp': 0, 'fn': 0, 'tp': 0, 'tn': 0}
for i,obs in enumerate(devin):
  if float(obs) < 0.5 and zach[i] < 0.5:
    irr_conmat['tn'] += 1
  elif float(obs) < 0.5 and zach[i] > 0.5:
    irr_conmat['fp'] += 1
  elif float(obs) > 0.5 and zach[i] > 0.5:
    irr_conmat['tp'] += 1
  elif float(obs) > 0.5 and zach[i] < 0.5:
    irr_conmat['fn'] += 1

good_models = []
good_predictions = []
for i,model in enumerate(models):
  if sensitivity(conmats[i]) > 0.5 and specificity(conmats[i]) > 0.5:
    good_models.append(model)
    good_predictions.append(predictions[i])

good_conmats = []
for guesses in good_predictions:
  conmat = {'fp': 0, 'fn': 0, 'tp': 0, 'tn': 0}
  for i,obs in enumerate(observations):
    if float(obs[-2]) < 0.5 and guesses[i] < 0.55:
      conmat['tn'] += 1
    elif float(obs[-2]) < 0.5 and guesses[i] > 0.65:
      conmat['fp'] += 1
    elif float(obs[-2]) > 0.5 and guesses[i] > 0.55:
      conmat['tp'] += 1
    elif float(obs[-2]) > 0.5 and guesses[i] < 0.65:
      conmat['fn'] += 1
  good_conmats.append(conmat)

guesses = np.matrix(good_predictions).transpose().tolist()
good_conmat = {'fp': 0, 'fn': 0, 'tp': 0, 'tn': 0}
failed_to_classify = 0
for i,obs in enumerate(observations):
  solid_guesses = [el for el in guesses[i] if abs(el-0.5) > 0.2]
  if len(solid_guesses) == 0:
    failed_to_classify += 1
  elif float(obs[-2]) < 0.5 and np.mean(solid_guesses) < 0.75:
    good_conmat['tn'] += 1
  elif float(obs[-2]) < 0.5 and np.mean(solid_guesses) > 0.25:
    good_conmat['fp'] += 1
  elif float(obs[-2]) > 0.5 and np.mean(solid_guesses) > 0.75:
    good_conmat['tp'] += 1
  elif float(obs[-2]) > 0.5 and np.mean(solid_guesses) < 0.25:
    good_conmat['fn'] += 1
  else:
    failed_to_classify += 1





[accuracy(conmat) for conmat in good_conmats]
[sensitivity(conmat) for conmat in good_conmats]
[specificity(conmat) for conmat in good_conmats]
[precision(conmat) for conmat in good_conmats]
[recall(conmat) for conmat in good_conmats]
[conmat for conmat in conmats if sensitivity(conmat) > 0.5 and specificity(conmat) > 0.5]
accuracy(conmat)
np.matrix([[el[0] for el in x.tolist()] for x in predictions]).transpose()

accuracy(conmat)
accuracy(irr_conmat)
sensitivity(conmat)
sensitivity(irr_conmat)
specificity(conmat)
specificity(irr_conmat)
precision(conmat)
precision(irr_conmat)
recall(conmat)
recall(irr_conmat)
