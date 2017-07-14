cd $(git rev-parse --show-toplevel)
echo $(pwd)
./commands/mkdirs.sh
./commands/download.sh
./commands/extract_background.sh
./commands/extract_altright_screen_names.sh
ruby commands/extract_altright_content.rb
./commands_test/concat_content.sh
