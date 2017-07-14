cd $(git rev-parse --show-toplevel)
echo $(pwd)

cat $(pwd)/baumgartner_data_test/comments_altright/* > $(pwd)/baumgartner_data_test/all_altright_user_comments.csv
cat $(pwd)/baumgartner_data_test/submissions_altright/* > $(pwd)/baumgartner_data_test/all_altright_user_submissions.csv
cat $(pwd)/baumgartner_data_test/comments_background/* > $(pwd)/baumgartner_data_test/all_background_user_comments.csv
cat $(pwd)/baumgartner_data_test/submissions_background/* > $(pwd)/baumgartner_data_test/all_background_user_submissions.csv