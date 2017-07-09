require 'csv'
filepath = `git rev-parse --show-toplevel`.strip
load filepath+'/array.rb'
background_counts = {}
`ls #{filepath}/baumgartner_data/comments_background/`.split("\n").each do |file|
  puts file
  begin
    background_file = CSV.read("#{filepath}/baumgartner_data/comments_background/#{file}");false
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
`ls #{filepath}/baumgartner_data/comments_altright/`.split("\n").each do |file|
  puts file
  puts altright_data.count
    background_file = CSV.read("#{filepath}/baumgartner_data/comments_altright/#{file}", col_sep: ",", row_sep: "\n");false
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
`ls #{filepath}/baumgartner_data/comments_altright/`.split("\n").each do |file|
  puts file
  begin
    background_file = CSV.read("#{filepath}/baumgartner_data/comments_altright/#{file}");false
    altright = background_file.select{|x| x[1] == "altright"};false
    altright.collect{|a| altright_comments << a}
  rescue
    next
  end
end;false

background_comments = []
`ls #{filepath}/baumgartner_data/comments_background/`.split("\n").each do |file|
  puts file
  begin
    background_file = CSV.read("#{filepath}/baumgartner_data/comments_background/#{file}");false
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

terms = top_terms_altright|top_terms_background;false
background_sample = background_comments.shuffle.first(1000);false
altright_sample = altright_comments.shuffle.first(1000);false

background_test = background_comments.shuffle.first(10000);false
altright_test = altright_comments.shuffle.first(10000);false


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



sample_altright_counts = altright_sample.collect{|x| [1, keyword_groups.collect{|kg| (kg & x.last.downcase.split(/[^[[:word:]]]+/)).length}].flatten}
sample_background_counts = background_sample.collect{|x| [0, keyword_groups.collect{|kg| (kg & x.last.downcase.split(/[^[[:word:]]]+/)).length}].flatten}
dataset = CSV.open("altright_machine_learning_dataset_train.csv", "w")
sample_altright_counts.each do |row|
  dataset << row
end
sample_background_counts.each do |row|
  dataset << row
end
dataset.close

test_altright_counts = altright_test.collect{|x| [1, keyword_groups.collect{|kg| (kg & x.last.downcase.split(/[^[[:word:]]]+/)).length}].flatten}
test_background_counts = background_test.collect{|x| [0, keyword_groups.collect{|kg| (kg & x.last.downcase.split(/[^[[:word:]]]+/)).length}].flatten}
dataset = CSV.open("altright_machine_learning_dataset_test.csv", "w")
test_altright_counts.each do |row|
  dataset << row
end
test_background_counts.each do |row|
  dataset << row
end
dataset.close


dataset = CSV.open("altright_machine_learning_dataset.csv", "w")
dataset << ["is_altright_comment", terms].flatten
altright_comments.each do |comment|
  counts = comment.last.downcase.downcase.split(/[^[[:word:]]]+/).counts
  dataset << [1, terms.collect{|t| counts[t]||0}].flatten
end;false
background_comments.each do |comment|
  counts = comment.last.downcase.downcase.split(/[^[[:word:]]]+/).counts
  dataset << [0, terms.collect{|t| counts[t]||0}].flatten
end;false
dataset.close
