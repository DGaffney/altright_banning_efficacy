import json
import os
import argparse
import numpy as np
import h5py
import keras_data_helpers
from keras_w2v import train_word2vec

from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Input, MaxPooling1D, Convolution1D, Embedding
from keras.layers.merge import Concatenate
from keras.datasets import imdb
from keras.preprocessing import sequence
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", help="dataset to sanitize ('background' or 'inner')")
ap.add_argument("-t", "--test", help="is test? Add in option if it's a test otherwise leave empty")
args = vars(ap.parse_args())

# ---------------------- Parameters section -------------------
#
# Model type. See Kim Yoon's Convolutional Neural Networks for Sentence Classification, Section 3
model_type = "CNN-non-static"  # CNN-rand|CNN-non-static|CNN-static

# Data source
data_source = "keras_data_set"  # keras_data_set|local_dir

# Model Hyperparameters
embedding_dim = 50
filter_sizes = (3, 8)
num_filters = 10
dropout_prob = (0.5, 0.8)
hidden_dims = 50

# Training parameters
batch_size = 64
num_epochs = 10

# Prepossessing parameters
sequence_length = 400
max_words = 5000

# Word2Vec parameters (see train_word2vec)
min_word_count = 1
context = 10
def load_data(path, dataset):
  x, y, vocabulary, vocabulary_inv_list = keras_data_helpers.load_data(path, dataset)
  vocabulary_inv = {key: value for key, value in enumerate(vocabulary_inv_list)}
  y = y.argmax(axis=1)
  # Shuffle data
  shuffle_indices = np.random.permutation(np.arange(len(y)))
  x = x[shuffle_indices]
  y = y[shuffle_indices]
  return x, y, vocabulary, vocabulary_inv

args["dataset"] = "inner"
dataset = args["dataset"]
prefix = '' if args["test"] == None else '_test'
filepath = os.popen('git rev-parse --show-toplevel').read().strip()
path = filepath+"/baumgartner_data"+prefix+"/machine_learning_resources"
x, y, vocabulary, vocabulary_inv = load_data(path, dataset)
if sequence_length != x.shape[1]:
    print("Adjusting sequence length for actual size")
    sequence_length = x.shape[1]

print("Vocabulary Size: {:d}".format(len(vocabulary_inv)))
# Prepare embedding layer weights and convert inputs for static model
print("Model type is", model_type)
with open(path+"/"+dataset+'_vocabulary.json', 'w') as outfile:
    json.dump(vocabulary, outfile)

with open(path+"/"+dataset+'_vocabulary_inv.json', 'w') as outfile:
    json.dump(vocabulary_inv, outfile)

for i in range(100):
  if model_type in ["CNN-non-static", "CNN-static"]:
      embedding_weights = train_word2vec(np.vstack((x)), vocabulary_inv, num_features=embedding_dim,
                                         min_word_count=min_word_count, context=context)
      if model_type == "CNN-static":
          x = np.stack([np.stack([embedding_weights[word] for word in sentence]) for sentence in x])
          print("x static shape:", x.shape)
  
  if model_type == "CNN-static":
      input_shape = (sequence_length, embedding_dim)
  else:
      input_shape = (sequence_length,)
  
  model_input = Input(shape=input_shape)
  if model_type == "CNN-static":
      z = model_input
  else:
      z = Embedding(len(vocabulary_inv), embedding_dim, input_length=sequence_length, name="embedding")(model_input)
  
  z = Dropout(dropout_prob[0])(z)
  # Convolutional block
  conv_blocks = []
  for sz in filter_sizes:
      conv = Convolution1D(filters=num_filters,
                           kernel_size=sz,
                           padding="valid",
                           activation="relu",
                           strides=1)(z)
      conv = MaxPooling1D(pool_size=2)(conv)
      conv = Flatten()(conv)
      conv_blocks.append(conv)
  
  z = Concatenate()(conv_blocks) if len(conv_blocks) > 1 else conv_blocks[0]
  z = Dropout(dropout_prob[1])(z)
  z = Dense(hidden_dims, activation="relu")(z)
  model_output = Dense(1, activation="sigmoid")(z)
  model = Model(model_input, model_output)
  model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
  if model_type == "CNN-non-static":
      weights = np.array([v for v in embedding_weights.values()])
      print("Initializing embedding layer with word2vec weights, shape", weights.shape)
      embedding_layer = model.get_layer("embedding")
      embedding_layer.set_weights([weights])
  model.fit(x, y, batch_size=batch_size, epochs=num_epochs)
  model.save(path+"/"+dataset+"_neural_net_voter_"+str(i)+".hdf5")
