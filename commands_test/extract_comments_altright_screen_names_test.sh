cd $(git rev-parse --show-toplevel)
echo $(pwd)

bzip2 -dck $(pwd)/baumgartner_data_test/comments_raw/RC_2016-11.bz2 | jq  -r ' select(.subreddit=="altright") | select(.author!="[deleted]") | .author' > $(pwd)/baumgartner_data_test/comments_altright_screen_names/RC_2016-11.csv
