require 'pry'
require 'csv'
require 'sidekiq'
FILEPATH = `git rev-parse --show-toplevel`.strip
class ExtractAltrightContent
  include Sidekiq::Worker
  sidekiq_options queue: :extract_altright_content
  def perform(file, prefix="")
    if file.include?("RS_")
      ALTRIGHT_USERS.each_slice(100) do |user_slice|
        `bzip2 -dck #{FILEPATH}/baumgartner_data#{prefix}/submissions_raw/#{file} | jq -r 'select([.author] | inside([\"#{user_slice.join('", "')}\"])) | [(.created_utc | tostring), .subreddit, .author, .id, .selftext, .title] | @csv' >> #{FILEPATH}/baumgartner_data#{prefix}/submissions_altright/#{file.split(".").first}.csv`
      end
    elsif file.include?("RC_")
      ALTRIGHT_USERS.each_slice(100) do |user_slice|
        `bzip2 -dck #{FILEPATH}/baumgartner_data#{prefix}/comments_raw/#{file} | jq -r 'select([.author] | inside([\"#{user_slice.join('", "')}\"])) | [(.created_utc | tostring), .subreddit, .author, .id, .parent_id, .body] | @csv' >> #{FILEPATH}/baumgartner_data#{prefix}/comments_altright/#{file.split(".").first}.csv`
      end
    end
  end

  def self.parse_missing_files(prefix="")
    ALTRIGHT_USERS.each_slice(100) do |user_slice|
      `bzip2 -dck #{FILEPATH}/baumgartner_data#{prefix}/submissions_raw/missing_subreddits_0-10m.json.bz2 | jq -r 'select([.author] | inside([\"#{user_slice.join('", "')}\"])) | [(.created_utc | tostring), .subreddit, .author, .id, .selftext, .title] | @csv' >> #{FILEPATH}/baumgartner_data#{prefix}/submissions_altright/missing_subreddits_0-10m.csv`
      `bzip2 -dck #{FILEPATH}/baumgartner_data#{prefix}/comments_raw/missing_comments.json.bz2 | jq -r 'select([.author] | inside([\"#{user_slice.join('", "')}\"])) | [(.created_utc | tostring), .subreddit, .author, .id, .selftext, .title] | @csv' >> #{FILEPATH}/baumgartner_data#{prefix}/comments_altright/missing_comments.csv`
    end
  end
  
  def self.kickoff_parallel
    #note that this requires running Sidekiq: in the commands folder, run `sidekiq -r ./generate_altright_timelines.rb -q extract_altright_content -c 50` to run 50 instances in parallel. redis-server must also be running on the machine in order for this to work. For additional information about sidekiq, please consult https://github.com/mperham/sidekiq. Note that this is not run in the test command set, and is only used when processing the entire reddit corpus.
    `ls #{FILEPATH}/baumgartner_data/submissions_raw`.split("\n").select{|f| f.include?("RS_")}.collect{|x| ExtractAltrightContent.perform_async(x)}
    `ls #{FILEPATH}/baumgartner_data/comments_raw`.split("\n").select{|f| f.include?("RC_")}.collect{|x| ExtractAltrightContent.perform_async(x)}
    self.parse_missing_files
  end
  
  def self.kickoff_sequential
    `ls #{FILEPATH}/baumgartner_data/submissions_raw`.split("\n").select{|f| f.include?("RS_")}.collect{|x| ExtractAltrightContent.new.perform(x)}
    `ls #{FILEPATH}/baumgartner_data/comments_raw`.split("\n").select{|f| f.include?("RC_")}.collect{|x| ExtractAltrightContent.new.perform(x)}
    self.parse_missing_files
  end
  
  def self.kickoff_sequential_test
    `ls #{FILEPATH}/baumgartner_data_test/submissions_raw`.split("\n").select{|f| f.include?("RS_")}.collect{|x| ExtractAltrightContent.new.perform(x, "_test")}
    `ls #{FILEPATH}/baumgartner_data_test/comments_raw`.split("\n").select{|f| f.include?("RC_")}.collect{|x| ExtractAltrightContent.new.perform(x, "_test")}
  end
end


if $0 == __FILE__ && ARGV.empty?
  ALTRIGHT_USERS = CSV.read(FILEPATH+"/baumgartner_data/altrighter_screen_names_uniq.csv").flatten
  ExtractAltrightContent.kickoff_sequential 
elsif $0 == __FILE__ && ARGV[0] == "test"
  ALTRIGHT_USERS = CSV.read(FILEPATH+"/baumgartner_data_test/altrighter_screen_names_uniq.csv").flatten
  ExtractAltrightContent.kickoff_sequential_test 
end
