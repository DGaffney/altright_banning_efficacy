cd $(git rev-parse --show-toplevel)
echo $(pwd)

./baumgartner_data/commands/extract_comments_altright_screen_names.sh
./baumgartner_data/commands/extract_submissions_altright_screen_names.sh
cat $(pwd)/baumgartner_data/submissions_altright_screen_names/* >> $(pwd)/baumgartner_data/altrighter_screen_names.csv
cat $(pwd)/baumgartner_data/comments_altright_screen_names/* >> $(pwd)/baumgartner_data/altrighter_screen_names.csv
mkdir $(pwd)/tmp
LC_ALL=C sort -nt',' -k1,1 -T $(pwd)/tmp $(pwd)/baumgartner_data/altrighter_screen_names.csv | uniq > $(pwd)/baumgartner_data/altrighter_screen_names_uniq.csv