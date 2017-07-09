cd $(git rev-parse --show-toplevel)
echo $(pwd)

wget http://files.pushshift.io/reddit/submissions/RS_2016-11.bz2
mv RS_2016-11.bz2 $(pwd)/baumgartner_data/submissions_raw/RS_2016-11.bz2
