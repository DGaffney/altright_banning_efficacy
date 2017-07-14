import os
import json
import tensorflow as tf
from tensorflow.contrib import lookup
from tensorflow.python.platform import gfile

def read_csv_str(filename):
  dataset = []
  i = 0
  with open(filename, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        dataset.append(row)
  return dataset

dataset = "inner"
filepath = os.popen('git rev-parse --show-toplevel').read().strip()
keyword_groups = [set(el) for el in json.loads(open(filepath+"/baumgartner_data/machine_learning_resources/"+dataset+"_keyword_groups.json").read())]
raw_dataset = read_csv_str(filepath+"/baumgartner_data/machine_learning_resources/"+dataset+"_dataset.csv")
human_votes = read_csv_str(filepath+"/baumgartner_data/machine_learning_resources/"+dataset+"_human_votes.csv")
MAX_DOCUMENT_LENGTH = sorted([len(r[0].split(" ")) for r in human_votes])[-1]
PADWORD = 'ZYXWZYXWZYXWZYXWZYXWZYXWZYXW'

# create vocabulary
vocab_processor = tf.contrib.learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
vocab_processor.fit([r[0] for r in human_votes])
with gfile.Open('vocab.tsv', 'wb') as f:
    f.write("{}\n".format(PADWORD))
    for word, index in vocab_processor.vocabulary_._mapping.iteritems():
      f.write("{}\n".format(word))

N_WORDS = len(vocab_processor.vocabulary_)
table = lookup.index_table_from_file(vocabulary_file='vocab.tsv', num_oov_buckets=1, vocab_size=None, default_value=-1)
titles = tf.constant([r[0] for r in human_votes])
words = tf.string_split(titles)
densewords = tf.sparse_tensor_to_dense(words, default_value=PADWORD)
numbers = table.lookup(densewords)
padding = tf.constant([[0,0],[0,MAX_DOCUMENT_LENGTH]])
padded = tf.pad(numbers, padding)
sliced = tf.slice(padded, [0,0], [-1, MAX_DOCUMENT_LENGTH])
EMBEDDING_SIZE = 10
embeds = tf.contrib.layers.embed_sequence(sliced, vocab_size=N_WORDS, embed_dim=EMBEDDING_SIZE)
WINDOW_SIZE = EMBEDDING_SIZE
STRIDE = int(WINDOW_SIZE/2)
conv = tf.contrib.layers.conv2d(embeds, 1, WINDOW_SIZE, 
                stride=STRIDE, padding='SAME') # (?, 4, 1)    
conv = tf.nn.relu(conv) # (?, 4, 1)    
words = tf.squeeze(conv, [2]) # (?, 4)
n_classes = len(TARGETS)     
logits = tf.contrib.layers.fully_connected(words, n_classes, 
                                    activation_fn=None)