#export SCRIPT_PATH = git rev-parse --show-toplevel
cd $(git rev-parse --show-toplevel)
echo $(pwd)

./baumgartner_data/commands/download_comments_test.sh
./baumgartner_data/commands/download_submissions_test.sh
