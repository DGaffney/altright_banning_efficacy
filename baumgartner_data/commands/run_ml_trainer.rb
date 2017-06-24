require 'csv'
filepath = `git rev-parse --show-toplevel`.strip
FILEPATH = filepath
load filepath+'/array.rb'
class RunMLTrainer
  include Sidekiq::Worker
  sidekiq_options queue: :train_ml_altright
  def perform
    rand_val = rand(100000000000)
    raw_dataset = CSV.read("#{FILEPATH}/baumgartner_data/machine_learning/altright_machine_learning_dataset_train_raw.csv");false
    raw_altright_comments = raw_dataset.select{|x| x[1] == "altright"};false
    raw_background_comments = raw_dataset.select{|x| x[1] != "altright"};false
    sampled_ar = raw_altright_comments.shuffle.first(1000)
    sampled_bg = raw_background_comments.shuffle.first(1000)
    keyword_groups = JSON.parse(File.read("#{FILEPATH}/baumgartner_data/machine_learning/keyword_groups.json"));false
    csv = CSV.open("#{FILEPATH}/baumgartner_data/machine_learning/ml_test_#{rand_val}_raw_comments.csv", "w")
    sampled_ar.each do |row|
      csv << row
    end;false
    sampled_bg.each do |row|
      csv << row
    end;false
    csv.close
    sample_altright_counts = sampled_ar.collect{|x| row = x.last.downcase.split(/[^[[:word:]]]+/);[1, keyword_groups.collect{|kg| (kg & row).length}].flatten}
    sample_background_counts = sampled_bg.collect{|x| row = x.last.downcase.split(/[^[[:word:]]]+/);[0, keyword_groups.collect{|kg| (kg & row).length}].flatten}
    dataset = CSV.open("#{filepath}/baumgartner_data/machine_learning/ml_test_#{rand_val}_ml_comments.csv", "w")
    sample_altright_counts.each do |row|
      dataset << row
    end
    sample_background_counts.each do |row|
      dataset << row
    end
    dataset.close    
  end
  
  def self.setup_data_asset
    background_counts = {}
    `ls #{FILEPATH}/baumgartner_data/comments_background/`.split("\n").each do |file|
      puts file
      begin
        background_file = CSV.read("#{FILEPATH}/baumgartner_data/comments_background/#{file}");false
        background_file.collect(&:last).collect(&:downcase).collect{|s| s.split(/[^[[:word:]]]+/)}.flatten.counts.each do |word, count|
          background_counts[word] ||= 0
          background_counts[word] += count
        end
      rescue
        next
      end
    end;false
    altright_counts = {}
    altright_data = []
    `ls #{FILEPATH}/baumgartner_data/comments_altrighters/`.split("\n").each do |file|
      puts file
      puts altright_data.count
        background_file = CSV.read("#{FILEPATH}/baumgartner_data/comments_altrighters/#{file}", col_sep: ",", row_sep: "\n");false
        altright = background_file.select{|x| x[1] == "altright"};false
        altright.collect{|ar| altright_data << ar}
        altright.collect(&:last).collect(&:downcase).collect{|s| s.split(/[^[[:word:]]]+/)}.flatten.counts.each do |word, count|
          altright_counts[word] ||= 0
          altright_counts[word] += count
        end
    end;false
    background_sum = background_counts.values.sum
    altright_sum = altright_counts.values.sum
    representativeness = Hash[altright_counts.collect{|k,v| [k, (v/altright_sum.to_f)/((background_counts[k]||1)/background_sum)]}];false
    altright_comments = []
    `ls #{FILEPATH}/baumgartner_data/comments_altrighters/`.split("\n").each do |file|
      puts file
      begin
        background_file = CSV.read("#{FILEPATH}/baumgartner_data/comments_altrighters/#{file}");false
        altright = background_file.select{|x| x[1] == "altright"};false
        altright.collect{|a| altright_comments << a}
      rescue
        next
      end
    end;false
    background_comments = []
    `ls #{FILEPATH}/baumgartner_data/comments_background/`.split("\n").each do |file|
      puts file
      begin
        background_file = CSV.read("#{FILEPATH}/baumgartner_data/comments_background/#{file}");false
        background_file.each do |row|
          if rand < 0.1
            background_comments << row
          end
        end
      rescue
        next
      end
    end;false
    top_rare_terms_altright = representativeness.select{|k,v| v > 2 && (background_counts[k]||0)/background_sum > 0.0001}.sort_by{|k,v| v}.reverse.collect(&:first);false
    top_terms_altright = representativeness.select{|k,v| v > 1 && (altright_counts[k]||0)/altright_sum > 0.001}.sort_by{|k,v| v}.reverse.collect(&:first);false
    top_terms_background = representativeness.select{|k,v| v < 1 && (background_counts[k]||0)/background_sum > 0.0001}.sort_by{|k,v| v}.collect(&:first);false
    background_comments.select{|x| (x.last.downcase.split(/[^[[:word:]]]+/) & top_rare_terms_altright & top_terms_altright).length > 1}.count
    altright_comments.select{|x| (x.last.downcase.split(/[^[[:word:]]]+/) & top_rare_terms_altright & top_terms_altright).length > 1}.count
    background_comments.collect{|x| (x.last.downcase.split(/[^[[:word:]]]+/) & top_rare_terms_altright & top_terms_altright).length}.average
    altright_comments.collect{|x| (x.last.downcase.split(/[^[[:word:]]]+/) & top_rare_terms_altright & top_terms_altright).length}.average
    rare_altright_only = representativeness.select{|k,v| v > 1 && (background_counts[k]||0)/background_sum < 0.0001}.sort_by{|k,v| v}.reverse.collect(&:first);false
    altright_comments.select{|x| (x.last.downcase.split(/[^[[:word:]]]+/) & rare_altright_only).length > 0}.count
    gapness = Hash[altright_counts.collect{|k,v| [k, (v/altright_sum.to_f)-((background_counts[k]||1)/background_sum)]}];false
#    background_sample = background_comments.shuffle.first(1000);false
#    altright_sample = altright_comments.shuffle.first(1000);false
#    background_test = background_comments.shuffle.first(10000);false
#    altright_test = altright_comments.shuffle.first(10000);false
    keyword_groups = [
    representativeness.select{|k,v| v > 2}.keys,
    representativeness.select{|k,v| v > 1 && altright_counts[k] > 100}.keys,
    representativeness.select{|k,v| v > 2 && (background_counts[k]||0)/background_sum < 0.0001}.keys,
    representativeness.select{|k,v| v > 2 && (background_counts[k]||0)/background_sum > 0.0001}.keys,
    gapness.select{|k,v| v > 0}.keys,
    gapness.select{|k,v| v > 1.6625465251303116e-07}.keys,
    gapness.select{|k,v| v > 0 && (background_counts[k]||0)/background_sum < 0.0001}.keys,
    altright_counts.sort_by{|k,v| v}.reverse.first(100).collect(&:first) - background_counts.sort_by{|k,v| v}.reverse.first(100).collect(&:first),
    altright_counts.sort_by{|k,v| v}.reverse.first(1000).collect(&:first) - background_counts.sort_by{|k,v| v}.reverse.first(1000).collect(&:first),
    representativeness.select{|k,v| v < 0.5}.keys,
    representativeness.select{|k,v| v < 1 && background_counts[k] > 100}.keys,
    representativeness.select{|k,v| v < 0.5 && (background_counts[k]||0)/background_sum > 0.0001}.keys,
    representativeness.select{|k,v| v < 0.5 && (altright_counts[k]||0)/altright_sum > 0.0001}.keys,
    gapness.select{|k,v| v < 0}.keys,
    gapness.select{|k,v| v < -1.199021482828853e-06}.keys,
    gapness.select{|k,v| v < 0 && (background_counts[k]||0)/background_sum > 0.0001}.keys,
    background_counts.sort_by{|k,v| v}.reverse.first(100).collect(&:first) - altright_counts.sort_by{|k,v| v}.reverse.first(100).collect(&:first),
    background_counts.sort_by{|k,v| v}.reverse.first(1000).collect(&:first) - altright_counts.sort_by{|k,v| v}.reverse.first(1000).collect(&:first)];false
    dataset = CSV.open("#{FILEPATH}/baumgartner_data/machine_learning/altright_machine_learning_dataset_train_raw.csv", "w")
    altright_comments.each do |row|
      dataset << row
    end;false
    background_comments.each do |row|
      dataset << row
    end;false
    dataset.close
    f = File.open("#{FILEPATH}/baumgartner_data/machine_learning/keyword_groups.json", "w")
    f.write(keyword_groups.to_json)
    f.close
  end
end


