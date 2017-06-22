require 'csv'
require 'sidekiq'
FILEPATH = `git rev-parse --show-toplevel`.strip
ALTRIGHT_USERS = CSV.read(FILEPATH+"/baumgartner_data/altrighter_screen_names_uniq.csv").flatten
class ExtractAltrightContent
  include Sidekiq::Worker
  sidekiq_options queue: :extract_altright_content
  def perform(file)
    if file.include?("RS_")
      csv = CSV.open("#{FILEPATH}/baumgartner_data/submissions_altrighters/#{file}", "w")
      CSV.foreach("#{FILEPATH}/baumgartner_data//#{file}", col_sep: ",", row_sep: "\n") do |row|
        csv << row if ALTRIGHT_USERS.include?(row[2])
      end;false
      csv.close
    elsif file.include?("RC_")
      csv = CSV.open("#{FILEPATH}/baumgartner_data/comments_altrighters/#{file}", "w")
      CSV.foreach("/media/dgaff/Main/wehrwein_altright_content/comments/#{file}", col_sep: ",", row_sep: "\n") do |row|
        csv << row if ALTRIGHT_USERS.include?(row[2])
      end;false
      csv.close
    end
  end

  def self.parse_missing_files
    csv = CSV.open("/media/dgaff/Main/wehrwein_altright_content/comments_altrighters/missing.csv", "w")
    CSV.foreach("/media/dgaff/Main/wehrwein_altright_content/comments/missing.csv") do |row|
      csv << row if ALTRIGHT_USERS.include?(row[2])
    end;false
    csv.close
    csv = CSV.open("/media/dgaff/Main/wehrwein_altright_content/submissions_altrighters/missing.csv", "w")
    CSV.foreach("/media/dgaff/Main/wehrwein_altright_content/submissions/missing.csv") do |row|
      csv << row if ALTRIGHT_USERS.include?(row[2])
    end;false
    csv.close
  end
  
  def self.kickoff_parallel
  #note that this requires running Sidekiq: in the commands folder, run `sidekiq -r ./generate_altright_timelines.rb -q extract_altright_content -c 50` to run 50 instances in parallel. redis-server must also be running on the machine in order for this to work. For additional information about sidekiq, please consult https://github.com/mperham/sidekiq.
    `ls /media/dgaff/Main/wehrwein_altright_content/submissions`.split("\n").select{|x| x.include?("RS_")}.collect{|x| ExtractAltrightContent.perform_async(x)}
    `ls /media/dgaff/Main/wehrwein_altright_content/comments`.split("\n").select{|x| x.include?("RC_")}.collect{|x| ExtractAltrightContent.perform_async(x)}
    self.parse_missing_files
  end
  
  def self.kickoff_sequential
    `ls /media/dgaff/Main/wehrwein_altright_content/submissions`.split("\n").select{|x| x.include?("RS_")}.collect{|x| ExtractAltrightContent.perform_async(x)}
    `ls /media/dgaff/Main/wehrwein_altright_content/comments`.split("\n").select{|x| x.include?("RC_")}.collect{|x| ExtractAltrightContent.perform_async(x)}
    self.parse_missing_files
  end
end
"bzip2 -dck $(pwd)/baumgartner_data/submissions_raw/RS_2016-09.bz2 | jq  -r 'select([.author] | inside(["aquma", "MisterBreeze", "The_New_Ent"]))'"
"bzip2 -dck $(pwd)/baumgartner_data/submissions_raw/RS_2016-09.bz2 | jq  -r ' select(.author inside([\"#{["aquma", "MisterBreeze", "The_New_Ent"].join('", "')}\"]))'"
'select(.items | index("blue"))'