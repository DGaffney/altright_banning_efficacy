import numpy as np
import re
import itertools
from collections import Counter
from itertools import izip_longest
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

"""
Original taken from https://github.com/dennybritz/cnn-text-classification-tf
"""
def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    #stemmer code from  - not the quite right place for this job but it'll be needed somewhere.
    ps = PorterStemmer()
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r" \\\(  \\\(  \\\( ", " \(\(\( ", string)
    string = re.sub(r" \\\)  \\\)  \\\) ", " \)\)\) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    string = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', "<URL/>", string)
    string = re.sub(r"www", " ", string)
    string = re.sub(r"com", " ", string)
    string = re.sub(r"org", " ", string)
    return string.strip().lower()

def stem_word(word):
  if "ethnic" in word:
    return "ethnic"
  elif "ethno" in word:
    return "ethnic"
  elif "jew" in word:
    return "jew"
  elif "jewed" in word:
    return "jew"
  elif "jewified" in word:
    return "jew"
  elif word == "keked" or word == "topkek":
    return "kek"
  elif "goyim" in word:
    return "goy"
  elif "jq" in word:
    return "holocaust"
  elif "mexic" in word:
    return "mexico"
  elif word == "skype" or word == "joo" or word == "joos":
    return "joo"
  elif word == "negroid":
    return "negro"
  elif word == "racial":
    return "race"
  elif word == "racialist":
    return "race"
  elif word == "whiteopia":
    return "white"
  elif word == "genes" or word == "genetics" or word == "genotype" or word == "genotypical" or word == "geneticist":
    return "gene"
  elif word == "slavic":
    return "slav"
  elif word == "antifa":
    return "antifascist"
  elif word == "cuckold" or word == "cuckoldry" or word == "cuckoldery" or word == "cucky" or word == "cuckolding" or word == "cuckolded" or word == "cuckservative" or word == "cuckservatives":
    return "cuck"
  elif word == "lefty" or word == "lefties" or word == "leftist":
    return "left"
  elif word == "asian" or word == "asiatic":
    return "asia"
  elif word == "talmudic":
    return "talmud"
  elif word == "triggery":
    return "trigger"
  elif word == "immigration" or word == "immigrations" or word == "immigrants" or word == "emigration" or word == "emigrant" or word == "emigrants":
    return "immigrant"
  elif word == "nuffin":
    return "muffin"
  elif word == "dindu":
    return "negro"
  elif word == "abo" or word == "abos":
    return "negro"
  elif word == "libshit":
    return "left"
  elif word == "fashy" or word == "fashwave" or word == "fashies":
    return "fash"
  elif word == "shoah":
    return "holocaust"
  elif word == "14" or word == "88" or word == "1488":
    return "1488"
  return word

def load_data_and_labels(path, dataset):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    positive_examples = list(open(path+"/altright-"+dataset+".pos").readlines())
    positive_examples = [s.strip() for s in positive_examples]
    negative_examples = list(open(path+"/altright-"+dataset+".neg").readlines())
    negative_examples = [s.strip() for s in negative_examples]
    # Split by words
    x_text = positive_examples + negative_examples
    x_text = [clean_str(sent) for sent in x_text]
    x_text = [[PorterStemmer().stem(stem_word(word)) for word in s.split(" ")] for s in x_text]
    # Generate labels
    positive_labels = [[0, 1] for _ in positive_examples]
    negative_labels = [[1, 0] for _ in negative_examples]
    y = np.concatenate([positive_labels, negative_labels], 0)
    return [x_text, y]


def pad_sentences(sentences, sequence_length=-1, padding_word="<PAD/>"):
    """
    Pads all sentences to the same length. The length is defined by the longest sentence.
    Returns padded sentences.
    """
    if sequence_length == -1:
      sequence_length = max(len(x) for x in sentences)
    padded_sentences = []
    for i in range(len(sentences)):
        sentence = sentences[i]
        num_padding = sequence_length - len(sentence)
        new_sentence = sentence + [padding_word] * num_padding
        padded_sentences.append(new_sentence)
    return padded_sentences


def build_vocab(sentences):
    """
    Builds a vocabulary mapping from word to index based on the sentences.
    Returns vocabulary mapping and inverse vocabulary mapping.
    """
    # Build vocabulary
    word_counts = Counter(itertools.chain(*sentences))
    # Mapping from index to word
    vocabulary_inv = [x[0] for x in word_counts.most_common()]
    # Mapping from word to index
    vocabulary = {x: i for i, x in enumerate(vocabulary_inv)}
    return [vocabulary, vocabulary_inv]


def build_input_data(sentences, labels, vocabulary):
    """
    Maps sentencs and labels to vectors based on a vocabulary.
    """
    x = np.array([[vocabulary[word] for word in sentence] for sentence in sentences])
    y = np.array(labels)
    return [x, y]
    
def load_data(path, dataset):
    """
    Loads and preprocessed data for the MR dataset.
    Returns input vectors, labels, vocabulary, and inverse vocabulary.
    """
    # Load and preprocess data
    sentences, labels = load_data_and_labels(path, dataset)
    sentences_padded = pad_sentences(sentences)
    vocabulary, vocabulary_inv = build_vocab(sentences_padded)
    x, y = build_input_data(sentences_padded, labels, vocabulary)
    return [x, y, vocabulary, vocabulary_inv]


def batch_iter(data, batch_size, num_epochs):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int(len(data) / batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        shuffle_indices = np.random.permutation(np.arange(data_size))
        shuffled_data = data[shuffle_indices]
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]