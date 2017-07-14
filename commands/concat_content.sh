cd $(git rev-parse --show-toplevel)
echo $(pwd)

cat $(pwd)/baumgartner_data/comments_altright/* > $(pwd)/baumgartner_data/all_altright_user_comments.csv
cat $(pwd)/baumgartner_data/submissions_altright/* > $(pwd)/baumgartner_data/all_altright_user_submissions.csv
cat $(pwd)/baumgartner_data/comments_background/* > $(pwd)/baumgartner_data/all_background_user_comments.csv
cat $(pwd)/baumgartner_data/submissions_background/* > $(pwd)/baumgartner_data/all_background_user_submissions.csv