cd $(git rev-parse --show-toplevel)
echo $(pwd)

./commands/extract_comments_background.sh
./commands/extract_submissions_background.sh
