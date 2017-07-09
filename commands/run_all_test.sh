cd $(git rev-parse --show-toplevel)
echo $(pwd)
./baumgartner_data/commands/mkdirs.sh
./baumgartner_data/commands/download_test.sh
./baumgartner_data/commands/extract_background_test.sh
./baumgartner_data/commands/extract_altright_screen_names_test.sh
ruby baumgartner_data/commands/extract_altright_content.rb test
