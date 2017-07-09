cd $(git rev-parse --show-toplevel)
echo $(pwd)

wget http://files.pushshift.io/reddit/comments/RC_2016-11.bz2
mv RC_2016-11.bz2 $(pwd)/baumgartner_data_test/comments_raw/RC_2016-11.bz2
