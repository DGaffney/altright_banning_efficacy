cd $(git rev-parse --show-toplevel)
echo $(pwd)
bzip2 -dck $(pwd)/baumgartner_data_test/comments_raw/RC_2016-11.bz2 | awk 'BEGIN {srand()} !/^$/ { if (rand() <= .001) print $0}' | jq -r "[(.created_utc | tostring), .subreddit, .author, .id, .parent_id, .body] | @csv" > $(pwd)/baumgartner_data_test/comments_background/RC_2016-11.csv
