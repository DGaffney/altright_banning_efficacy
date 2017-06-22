require 'csv'
require 'sidekiq'
FILEPATH = `git rev-parse --show-toplevel`.strip
ALTRIGHT_USERS = CSV.read(FILEPATH+"/baumgartner_data/altrighter_screen_names_uniq.csv").flatten
class ExtractAltrightContent
  include Sidekiq::Worker
  sidekiq_options queue: :extract_altright_content
  def perform(file)
    if file.include?("RS_")
      ALTRIGHT_USERS.each_slice(100) do |user_slice|
        `bzip2 -dck #{FILEPATH}/baumgartner_data/submissions_raw/#{file} | jq -r 'select([.author] | inside([\"#{user_slice.join('", "')}\"])) | [(.created_utc | tostring), .subreddit, .author, .id, .selftext, .title] | @csv' >> #{FILEPATH}/baumgartner_data/submissions_altrighters/#{file.split(".").first}.csv`
      end
    elsif file.include?("RC_")
      ALTRIGHT_USERS.each_slice(100) do |user_slice|
        `bzip2 -dck #{FILEPATH}/baumgartner_data/comments_raw/#{file} | jq -r 'select([.author] | inside([\"#{user_slice.join('", "')}\"])) | [(.created_utc | tostring), .subreddit, .author, .id, .parent_id, .body] | @csv' >> #{FILEPATH}/baumgartner_data/comments_altrighters/#{file.split(".").first}.csv`
      end
    end
  end

  def self.parse_missing_files
    ALTRIGHT_USERS.each_slice(100) do |user_slice|
      `bzip2 -dck #{FILEPATH}/baumgartner_data/submissions_raw/missing_subreddits_0-10m.json.bz2 | jq -r 'select([.author] | inside([\"#{user_slice.join('", "')}\"])) | [(.created_utc | tostring), .subreddit, .author, .id, .selftext, .title] | @csv' >> #{FILEPATH}/baumgartner_data/submissions_altrighters/missing_subreddits_0-10m.csv`
      `bzip2 -dck #{FILEPATH}/baumgartner_data/comments_raw/missing_comments.json.bz2 | jq -r 'select([.author] | inside([\"#{user_slice.join('", "')}\"])) | [(.created_utc | tostring), .subreddit, .author, .id, .selftext, .title] | @csv' >> #{FILEPATH}/baumgartner_data/comments_altrighters/missing_comments.csv`
    end
  end
  
  def self.kickoff_parallel
    #note that this requires running Sidekiq: in the commands folder, run `sidekiq -r ./generate_altright_timelines.rb -q extract_altright_content -c 50` to run 50 instances in parallel. redis-server must also be running on the machine in order for this to work. For additional information about sidekiq, please consult https://github.com/mperham/sidekiq.
    `ls #{FILEPATH}/baumgartner_data/submissions_raw`.split("\n").select{|f| f.include?("RS_")}.collect{|x| ExtractAltrightContent.perform_async(x)}
    `ls #{FILEPATH}/baumgartner_data/comments_raw`.split("\n").select{|f| f.include?("RC_")}.collect{|x| ExtractAltrightContent.perform_async(x)}
    self.parse_missing_files
  end
  
  def self.kickoff_sequential
    `ls #{FILEPATH}/baumgartner_data/submissions_raw`.split("\n").select{|f| f.include?("RS_")}.collect{|x| ExtractAltrightContent.new.perform(x)}
    `ls #{FILEPATH}/baumgartner_data/comments_raw`.split("\n").select{|f| f.include?("RC_")}.collect{|x| ExtractAltrightContent.new.perform(x)}
    self.parse_missing_files
  end
end