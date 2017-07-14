sentences = keras_data_helpers.pad_sentences([keras_data_helpers.clean_str(r[0]).replace('  ', ' ').split() for r in human_votes])
labels = [int(r[1]) for r in human_votes]
x, y = keras_data_helpers.build_input_data(sentences, labels, vocabulary)