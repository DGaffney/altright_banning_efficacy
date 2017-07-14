#Alright Banning Efficacy Code

This code serves as a replication repository for a forthcoming paper by Devin Gaffney and Zach Wehrwein. In sum, the files in this repository should be sufficient to replicate data used in this paper, and may provide the basis by which other researchers may extend the work.

###Dependencies

This library has a slew of dependencies in order to properly work. We will step through them per each step of analysis we conducted on the Reddit Corpus:

1. Downloading the corpus: this repository presumes researchers have `wget`.
2. Extracting metadata from raw comments: we use `bzip2` to unzip the files in a stream, then `[jq](https://stedolan.github.io/jq/)` to extract fields of interest. 
3. To extract authors of altright Submissions and Comments, we use `sort` and `uniq`.
4. To extract the full corpus of content posted by these users, we presume the presence of ruby, and the ruby gems of `pry` and `sidekiq`. This can also be sped up by running this process in parallel - please consult `commands/extract_altright_content.rb`
5. To use the machine learning portion of this repository, we presume the presence of python, either `theano` or `tensorflow`, the library `keras` which is a scripting language built upon both `theano` and `tensorflow` (this has only been tested with `tensorflow`, we are careful to note), and in turn, to marshal out models to files you must install `h5py`, which also has apt-get distributables you'll need to install via `sudo apt-get install libhdf5-dev` on Ubuntu, as an example. Without this library, it will be impossible to store models to use as ensemble voters.
6. Our human codings are presented in this repository as given - you may feel free to develop your own coding schedules so long as they follow the format of baumgartner\_data/machine\_learning\_resources/{DATASET\_NAME}\_human\_votes.csv, and `-d` is specified as shown in commands/run\_all.sh and commands/run\_all\_test.sh in commands and commands\_test, respectively.
7. For any questions, clarifications, or errors in generating data, don't hesitate to open an issue. We look forward to making this a replicable study, and a generalized pattern of analyzing the baumgartner corpus.