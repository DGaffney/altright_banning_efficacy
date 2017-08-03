from nltk.stem import PorterStemmer
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
import sys
sys.setrecursionlimit(20000)
words = set()
import collections
word_counter = collections.Counter()
bot_list = ["SamMee514", "TweetPoster", "TotesMessenger", "youtubefactsbot", "autotldr", "gifv-bot", "Mentioned_Videos", "ConvertsToMetric", "OriginalPostSearcher", "sneakpeekbot", "xkcd_transcriber", "thank_mr_skeltal_bot", "HelperBot_", "image_linker_bot", "SmallSubBot", "JoeBidenBot", "autourbanbot", "PlaylisterBot", "ayylmao2dongerbot-v2", "TheWallGrows", "pm_me_your_bw_pics", "navigatorbot", "DailMail_Bot"]
for f in os.popen("ls "+filepath+"/baumgartner_data"+prefix+"/comments_altright").read().split("\n"):
  if f != '':
    print f
    for row in read_csv_str(filepath+"/baumgartner_data"+prefix+"/comments_altright/"+f):
      if row[2] not in bot_list:
        sent = row[5].strip()
        word_counter.update(keras_data_helpers.pad_sentences([[PorterStemmer().stem(keras_data_helpers.stem_word(word)) for word in keras_data_helpers.clean_str(sent).split(" ")]])[0])

#>>> len(words)
#2395897 Total unique words, total unique words in hand coded data
#753124951 Total word count, 717360001 total times known words used in total word count

path = filepath+"/baumgartner_data"+prefix+"/machine_learning_resources"
output = open(path+'/inner_full_altright_comments_vocabulary_inv.pkl', 'wb')
vocabulary_inv = [x[0] for x in word_counter.most_common()]
pickle.dump(vocabulary_inv, output)
output.close()
output = open(path+'/inner_full_altright_comments_vocabulary.pkl', 'wb')
vocabulary = {x: i for i, x in enumerate(vocabulary_inv)}
pickle.dump(vocabulary, output)
output.close()

human_votes = read_csv_str(filepath+"/baumgartner_data"+prefix+"/machine_learning_resources/"+dataset+"_human_votes_neural_net_expanded.csv")
data = [[PorterStemmer().stem(keras_data_helpers.stem_word(word)) for word in keras_data_helpers.clean_str(r[5]).split(" ")] for r in human_votes]
human_vote_words = set([item for sublist in data for item in sublist])
#>>> len(human_vote_words)
#11247

pos_votes = [[str.join(" ", [PorterStemmer().stem(keras_data_helpers.stem_word(word)) for word in keras_data_helpers.clean_str(r[5]).split(" ")]), r[-1]] for r in human_votes if float(r[-1]) == 1]
neg_votes = [[str.join(" ", [PorterStemmer().stem(keras_data_helpers.stem_word(word)) for word in keras_data_helpers.clean_str(r[5]).split(" ")]), r[-1]] for r in human_votes if float(r[-1]) == 0]
np.random.shuffle(pos_votes)
np.random.shuffle(neg_votes)
with open(filepath+"/baumgartner_data"+prefix+"/machine_learning_resources/altright-"+dataset+".pos", 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(pos_votes)

with open(filepath+"/baumgartner_data"+prefix+"/machine_learning_resources/altright-"+dataset+".neg", 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(neg_votes[:int(len(pos_votes)*1.5)])
