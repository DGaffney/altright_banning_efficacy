#export SCRIPT_PATH = git rev-parse --show-toplevel
cd $(git rev-parse --show-toplevel)
echo $(pwd)

./commands/download_comments.sh
./commands/download_submissions.sh
