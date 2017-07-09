cd $(git rev-parse --show-toplevel)
echo $(pwd)

bzip2 -dck $(pwd)/baumgartner_data_test/submissions_raw/RS_2016-11.bz2 | jq  -r ' select(.subreddit=="altright") | select(.author!="[deleted]") | .author' > $(pwd)/baumgartner_data_test/submissions_altright_screen_names/RS_2016-11.csv
