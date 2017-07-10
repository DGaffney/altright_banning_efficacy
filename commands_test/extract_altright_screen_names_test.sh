cd $(git rev-parse --show-toplevel)
echo $(pwd)

./commands_test/extract_comments_altright_screen_names_test.sh
./commands_test/extract_submissions_altright_screen_names_test.sh
cat $(pwd)/baumgartner_data_test/submissions_altright_screen_names/* >> $(pwd)/baumgartner_data_test/altrighter_screen_names.csv
cat $(pwd)/baumgartner_data_test/comments_altright_screen_names/* >> $(pwd)/baumgartner_data_test/altrighter_screen_names.csv
mkdir $(pwd)/tmp
LC_ALL=C sort -nt',' -k1,1 -T $(pwd)/tmp $(pwd)/baumgartner_data_test/altrighter_screen_names.csv | uniq > $(pwd)/baumgartner_data_test/altrighter_screen_names_uniq.csv