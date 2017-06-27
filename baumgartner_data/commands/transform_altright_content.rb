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
#    raw_dataset = CSV.read("#{FILEPATH}/baumgartner_data/comments_altrighters/#{file}", row_sep: "\n", col_sep: ",");false
#    return nil if raw_dataset.count == 0
#    keyword_groups = JSON.parse(File.read("#{FILEPATH}/baumgartner_data/machine_learning/keyword_groups.json"));false
#    csv = CSV.open("#{FILEPATH}/baumgartner_data/comments_altrighters_ml_transformed/#{file}", "w")
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
#    predicted = JSON.parse(`python #{FILEPATH}/baumgartner_data/commands/mark_all_comments_ml.py -f #{FILEPATH}/baumgartner_data/comments_altrighters_ml_transformed/#{file}`)
#    csv = CSV.open("#{FILEPATH}/baumgartner_data/comments_altrighters_ml_predicted/#{file}", "w")
#    raw_dataset.zip(predicted).each do |row|
#      csv << row.flatten
#    end
#    csv.close
  end
  
  def self.kickoff
    `mkdir #{FILEPATH}/baumgartner_data/comments_altrighters_ml_transformed`
    `ls #{FILEPATH}/baumgartner_data/comments_altrighters`.split("\n").each do |file|
      TransformAltrightContent.perform_async(file)
    end
  end
end