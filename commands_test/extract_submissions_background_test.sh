cd $(git rev-parse --show-toplevel)
echo $(pwd)

bzip2 -dck $(pwd)/baumgartner_data/submissions_raw/RS_2016-11.bz2  | awk 'BEGIN {srand()} !/^$/ { if (rand() <= .001) print $0}' | jq -r "[(.created_utc | tostring), .subreddit, .author, .id, .selftext, .title] | @csv" > $(pwd)/baumgartner_data/submissions_background/RS_2016-11.csv