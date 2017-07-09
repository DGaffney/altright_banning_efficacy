cd $(git rev-parse --show-toplevel)
echo $(pwd)
./baumgartner_data/commands/mkdirs.sh
./baumgartner_data/commands/download.sh
./baumgartner_data/commands/extract_background.sh
./baumgartner_data/commands/extract_altright_screen_names.sh
ruby baumgartner_data/commands/extract_altright_content.rb
