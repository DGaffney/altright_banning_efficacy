cd $(git rev-parse --show-toplevel)
echo $(pwd)

./baumgartner_data/commands/extract_comments_altrighters.sh
./baumgartner_data/commands/extract_submissions_altrighters.sh
