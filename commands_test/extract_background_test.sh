cd $(git rev-parse --show-toplevel)
echo $(pwd)

./commands_test/extract_comments_background_test.sh
./commands_test/extract_submissions_background_test.sh
