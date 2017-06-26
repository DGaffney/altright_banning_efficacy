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
    raw_dataset = CSV.read("#{FILEPATH}/baumgartner_data/comments_altrighters/#{file}", row_sep: "\n", col_sep: ",");false
    keyword_groups = JSON.parse(File.read("#{FILEPATH}/baumgartner_data/machine_learning/keyword_groups.json"));false
    csv = CSV.open("#{FILEPATH}/baumgartner_data/comments_altrighters_ml_transformed/#{file}", "w")
    ii = 0
    raw_dataset.each do |row|
      parsed = row.last.downcase.split(/[^[[:word:]]]+/)
      csv << keyword_groups.collect{|kg| (kg & parsed).length}
      ii += 1
      puts ii if ii % 1000 == 0
    end
    csv.close
    `python #{FILEPATH}/baumgartner_data/commands/mark_all_comments_ml.py -m #{FILEPATH}/baumgartner_data/commands/ml_model_altright.pkl -f #{FILEPATH}/baumgartner_data/comments_altrighters_ml_transformed/#{file}`
  end
  
  def self.kickoff
    `mkdir #{FILEPATH}/baumgartner_data/comments_altrighters_ml_transformed`
    `ls #{FILEPATH}/baumgartner_data/comments_altrighters`.split("\n").each do |file|
      TransformAltrightContent.perform_async(file)
    end
  end
end