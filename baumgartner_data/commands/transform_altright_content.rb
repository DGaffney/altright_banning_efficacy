require 'json'
require 'sidekiq'
require 'csv'
filepath = `git rev-parse --show-toplevel`.strip
FILEPATH = filepath
load filepath+'/array.rb'
class TransformAltrightContent
  include Sidekiq::Worker
  sidekiq_options queue: :train_ml_altright
  def perform(file)
    `python #{FILEPATH}/baumgartner_data/commands/mark_all_comments_ml.py -f #{file}`
    puts "python #{FILEPATH}/baumgartner_data/commands/mark_all_comments_ml.py -f #{file}"
#    raw_dataset = CSV.read("#{FILEPATH}/baumgartner_data/comments_altright/#{file}", row_sep: "\n", col_sep: ",");false
#    return nil if raw_dataset.count == 0
#    keyword_groups = JSON.parse(File.read("#{FILEPATH}/baumgartner_data/machine_learning/keyword_groups.json"));false
#    csv = CSV.open("#{FILEPATH}/baumgartner_data/comments_altright_ml_transformed/#{file}", "w")
#    ii = 0
#    raw_dataset.each do |row|
#      parsed = row.last.downcase.split(/[^[[:word:]]]+/)
#      csv << keyword_groups.collect{|kg| (kg & parsed).length}
#      keyword_groups.collect{|kg| (kg & parsed).length}
#      keyword_groups.collect{|kg| parsed.collect{|el| kg.index(el)}.compact.length}
#      ii += 1
#      puts ii if ii % 1000 == 0
#    end
#    csv.close
#    predicted = JSON.parse(`python #{FILEPATH}/baumgartner_data/commands/mark_all_comments_ml.py -f #{FILEPATH}/baumgartner_data/comments_altright_ml_transformed/#{file}`)
#    csv = CSV.open("#{FILEPATH}/baumgartner_data/comments_altright_ml_predicted/#{file}", "w")
#    raw_dataset.zip(predicted).each do |row|
#      csv << row.flatten
#    end
#    csv.close
  end
  
  def self.kickoff
    `mkdir #{FILEPATH}/baumgartner_data/comments_altright_ml_transformed`
    `ls #{FILEPATH}/baumgartner_data/comments_altright`.split("\n").each do |file|
      TransformAltrightContent.perform_async(file)
    end
  end
end
all_comments = CSV.read("single_file_predictions.csv");false
17090
`mkdir #{FILEPATH}/baumgartner_data/partitioned_predicted_altrighter_timelines.csv`
i = 0
csvs = {}
altright.each do |comment|
  csvs[(i % 1000).to_s] ||= CSV.open("#{FILEPATH}/baumgartner_data/partitioned_predicted_altrighter_timelines/#{i % 1000}", "w")
  csvs[(i % 1000).to_s] << comment
  i += 1
  puts i if i % 10000 == 0
end;false
not_altright_sample.each do |comment|
  csvs[(i % 1000).to_s] ||= CSV.open("#{FILEPATH}/baumgartner_data/partitioned_predicted_altrighter_timelines/#{i % 1000}", "w")
  csvs[(i % 1000).to_s] << comment
  i += 1
  puts i if i % 10000 == 0
end;false
#tmux tab 18
altright_hits = {}
altright_misses = {}
all_comments.each do |row|
  if row.last.to_i == 0
    altright_misses[row[1]] ||= 0
    altright_misses[row[1]] += 1
  elsif row.last.to_i == 1
    altright_hits[row[1]] ||= 0
    altright_hits[row[1]] += 1
  end
end;false
load '/media/dgaff/backup/Code/reddit_random_walk/code/extensions/array.rb'
subreddit_counts = Hash[CSV.read("/media/dgaff/backup/Code/reddit_random_walk/code/results/dataset_full/data/total_transitions_all_subreddits_all_time.csv").collect{|x| [x[0], x[1].to_i]}];false
altright_hit_density = altright_hits.values.sum
altright_miss_density = altright_misses.values.sum
background_altright_hits = Hash[altright_hits.keys.collect{|k| [k, subreddit_counts[k]||0]}];false
background_altright_hit_density = background_altright_hits.values.sum
background_altright_misses = Hash[altright_misses.keys.collect{|k| [k, subreddit_counts[k]||0]}];false
background_altright_miss_density = background_altright_misses.values.sum
ratio_hits = Hash[altright_hits.collect{|k,v| [k, (v/altright_hit_density)/((background_altright_hits[k]/background_altright_hit_density)+0.000001)] if v > 100}.compact]
ratio_misses = Hash[altright_misses.collect{|k,v| [k, (v/altright_miss_density)/((background_altright_misses[k]/background_altright_hit_density)+0.000001)] if v > 100}.compact]
final_hits = altright_hits.collect{|k,v| [k,v,ratio_hits[k]] if v > 100}.compact
final_misses = altright_misses.collect{|k,v| [k,v,ratio_misses[k]] if v > 100}.compact
csv = CSV.open("altright_hits.csv", "w")
final_hits.collect{|r| csv << r};false
csv.close
csv = CSV.open("altright_misses.csv", "w")
final_misses.collect{|r| csv << r};false
csv.close


all_comments_sorted = all_comments.sort_by{|r| r.first.to_i};false
user_timelines = {}
all_comments_sorted.each do |row|
  user_timelines[row[2]] ||= []
  user_timelines[row[2]] << row
end;false
cumulatives = {}
user_timelines.each do |k,v|
  post_count = 0
  flagged_count = 0
  cumulatives[k] ||= []
  v.each do |comment|
    if comment.last.to_i == 1
      flagged_count += 1
    end
    post_count += 1
    cumulatives[k] << flagged_count/post_count.to_f
  end
end;false
l = 2000
transposed = cumulatives.values.map{|e| e.values_at(0...l)}.transpose.collect(&:compact).collect{|arr| [arr.average, arr.count]};false
year_cohorts = {}
user_timelines.each do |k,v|
  year_cohorts[k] = Time.at(v.first.first.to_i).strftime("%Y")
end;false
year_cohort_transposed = {}
year_cohorts.values.uniq.each do |cohort_year|
  puts cohort_year
  users = year_cohorts.select{|k,v| v == cohort_year}.keys
  l = 2000
  year_cohort_transposed[cohort_year] = cumulatives.values_at(*users).map{|e| e.values_at(0...l)}.transpose.collect(&:compact).collect{|arr| [arr.average, arr.count]};false
end;false

f = File.open("cumulative_altright_adoption_count.json", "w")
f.write(transposed.to_json)
f.close
f = File.open("cumulative_altright_adoption_count_yearly_cohort.json", "w")
f.write(year_cohort_transposed.to_json)
f.close
daily_altrights = {}
daily_altright_misses = {}
all_comments.each do |comment|
  if comment.last.to_i == 1 && comment[1] != "altright"
    daily_altrights[Time.at(comment.first.to_i).strftime("%Y-%m-%d")] ||= {}
    daily_altrights[Time.at(comment.first.to_i).strftime("%Y-%m-%d")][comment[1]] ||= 0
    daily_altrights[Time.at(comment.first.to_i).strftime("%Y-%m-%d")][comment[1]] += 1
  elsif comment.last.to_i == 0 && comment[1] != "altright"
    daily_altright_misses[Time.at(comment.first.to_i).strftime("%Y-%m-%d")] ||= {}
    daily_altright_misses[Time.at(comment.first.to_i).strftime("%Y-%m-%d")][comment[1]] ||= 0
    daily_altright_misses[Time.at(comment.first.to_i).strftime("%Y-%m-%d")][comment[1]] += 1
  end
end;false
f = File.open("daily_altright_densities.json", "w")
f.write(daily_altrights.to_json)
f.close
f = File.open("daily_altright_miss_densities.json", "w")
f.write(daily_altright_misses.to_json)
f.close


edge_creations = {}
`ls /media/dgaff/backup/Code/dissertation_agent_based/Sandbox/larger_data/edge_creation/`.split("\n").each do |file|
  puts file
  CSV.read("/media/dgaff/backup/Code/dissertation_agent_based/Sandbox/larger_data/edge_creation/"+file).each do |row|
    edge_creations[row.first]||={}
    edge_creations[row.first][row.last] = true
  end
end;false
(`ls /media/dgaff/backup/Code/reddit_random_walk/code/results/dataset_full/data/baumgartner_time_transitions`.split("\n").select{|x| x.split("-").length == 3}-`ls /media/dgaff/backup/Code/dissertation_agent_based/Sandbox/larger_data/edge_creation/`.split("\n")).each do |file|
  puts file
  edges_created_today = {}
  unique_sorted_edges = CSV.parse(`cat /media/dgaff/backup/Code/reddit_random_walk/code/results/dataset_full/data/baumgartner_time_transitions/#{file} | awk -F ',' '{print $1","$2}' | LC_ALL=C sort -t',' -k1,1 -k2,2 | uniq`);false
  puts "Parsing Edges"
  unique_sorted_edges.each do |row|
    next if row[0] == row[1] or row[0].nil? or row[1].nil?
    if edge_creations[row.first].nil?
      edges_created_today[row.first] = {}
      edge_creations[row.first] = {}
    end
    if edge_creations[row.first][row[1]].nil?
      edges_created_today[row.first][row[1]] = true
      edge_creations[row.first][row[1]] = true
    end
  end
  puts "Writing CSV"
  csv_out = CSV.open("/media/dgaff/backup/Code/dissertation_agent_based/Sandbox/larger_data/edge_creation/#{file}", "w")
  edges_created_today.each do |k,v|
    v.keys.each do |key|
      csv_out << [k,key]
    end
  end
  csv_out.close
end

