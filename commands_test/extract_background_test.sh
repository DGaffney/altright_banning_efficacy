cd $(git rev-parse --show-toplevel)
echo $(pwd)

./baumgartner_data/commands/extract_comments_background_test.sh
./baumgartner_data/commands/extract_submissions_background_test.sh
