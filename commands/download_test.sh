#export SCRIPT_PATH = git rev-parse --show-toplevel
cd $(git rev-parse --show-toplevel)
echo $(pwd)

./commands_test/download_comments_test.sh
./commands_test/download_submissions_test.sh
