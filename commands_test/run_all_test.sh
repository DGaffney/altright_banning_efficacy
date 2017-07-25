cd $(git rev-parse --show-toplevel)
echo $(pwd)
./commands_test/mkdirs_test.sh
./commands_test/download_test.sh
./commands_test/extract_background_test.sh
./commands_test/extract_altright_screen_names_test.sh
ruby commands/extract_altright_content.rb test
./commands_test/concat_content.sh
python commands/generate_neural_net_corpus.py -d inner -t test
python commands/generate_neural_net_corpus.py -d background -t test
python commands/keras_neural_net_cross_validation.py -d inner -t test
python commands/keras_neural_net_cross_validation.py -d background -t test
python commands/keras_neural_net_internal_consistency.py -d inner -t test
python commands/keras_neural_net_internal_consistency.py -d background -t test
python commands/keras_generate_neural_net_models.py -d inner -t test -c 100
python commands/keras_generate_neural_net_models.py -d background -t test -c 100
python commands/keras_mark_all_comments.py -d inner -t test -c 100
python commands/keras_mark_all_comments.py -d background -t test -c 100
