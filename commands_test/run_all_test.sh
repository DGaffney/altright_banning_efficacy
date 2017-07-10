cd $(git rev-parse --show-toplevel)
echo $(pwd)
./commands_test/mkdirs_test.sh
./commands_test/download_test.sh
./commands_test/extract_background_test.sh
./commands_test/extract_altright_screen_names_test.sh
ruby commands_test/extract_altright_content.rb test
