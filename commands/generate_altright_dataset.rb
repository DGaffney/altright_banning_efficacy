require 'csv'
filepath = `git rev-parse --show-toplevel`.strip
load filepath+'/array.rb'
all_altright = []
`ls #{filepath}/baumgartner_data/comments_altright/`.split("\n").each do |file|
  puts file
  begin
    background_file = CSV.read("#{filepath}/baumgartner_data/comments_altright/#{file}", col_sep: ",", row_sep: "\n");false
    background_file.each do |row|
    all_altright << row
    end
  rescue
    next
  end
end;false
altright = all_altright.select{|x| x[1] == "altright"};false
not_altright = all_altright.select{|x| x[1] != "altright"};false
all_altright = []
altright_counts = {}
altright.each do |comment|
  comment.last.downcase.split(/[^[[:word:]]]+/).counts.reject{|k,v| k.empty?}.each do |word, count|
    altright_counts[word] ||= 0
    altright_counts[word] += count
  end
end;false
not_altright_counts = {}
not_altright_counts = {}
not_altright.shuffle.first(altright.length*2).each do |comment|
  comment.last.downcase.split(/[^[[:word:]]]+/).counts.reject{|k,v| k.empty?}.each do |word, count|
    not_altright_counts[word] ||= 0
    not_altright_counts[word] += count
  end
end;false
not_altright_sum = not_altright_counts.values.sum
altright_sum = altright_counts.values.sum
representativeness = Hash[altright_counts.collect{|k,v| [k, (v/altright_sum.to_f)/((not_altright_counts[k]||1)/not_altright_sum)]}];false
background_counts = not_altright_counts;false
background_sum = not_altright_counts.values.sum

top_rare_terms_altright = representativeness.select{|k,v| v > 2 && (background_counts[k]||0)/background_sum > 0.0001}.sort_by{|k,v| v}.reverse.collect(&:first);false
top_terms_altright = representativeness.select{|k,v| v > 1 && (altright_counts[k]||0)/altright_sum > 0.001}.sort_by{|k,v| v}.reverse.collect(&:first);false
top_terms_background = representativeness.select{|k,v| v < 1 && (background_counts[k]||0)/background_sum > 0.0001}.sort_by{|k,v| v}.collect(&:first);false
not_altright.select{|x| (x.last.downcase.split(/[^[[:word:]]]+/) & top_rare_terms_altright & top_terms_altright).length > 1}.count
altright.select{|x| (x.last.downcase.split(/[^[[:word:]]]+/) & top_rare_terms_altright & top_terms_altright).length > 1}.count
not_altright.collect{|x| (x.last.downcase.split(/[^[[:word:]]]+/) & top_rare_terms_altright & top_terms_altright).length}.average
altright.collect{|x| (x.last.downcase.split(/[^[[:word:]]]+/) & top_rare_terms_altright & top_terms_altright).length}.average
rare_altright_only = representativeness.select{|k,v| v > 1 && (background_counts[k]||0)/background_sum < 0.0001}.sort_by{|k,v| v}.reverse.collect(&:first);false
altright.select{|x| (x.last.downcase.split(/[^[[:word:]]]+/) & rare_altright_only).length > 0}.count
gapness = Hash[altright_counts.collect{|k,v| [k, (v/altright_sum.to_f)-((background_counts[k]||1)/background_sum)]}];false

terms = top_terms_altright|top_terms_background;false
background_sample = not_altright.shuffle.first(1000);false
altright_sample = altright.shuffle.first(1000);false


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

require 'json'
f = File.open("inner_altright_machine_learning_keyword_groups.json", "w");false
f.write(keyword_groups.to_json)
f.close
sample_altright_counts = altright_sample.collect{|x| [1, keyword_groups.collect{|kg| (kg & x.last.downcase.split(/[^[[:word:]]]+/)).length}].flatten}
sample_background_counts = background_sample.collect{|x| [0, keyword_groups.collect{|kg| (kg & x.last.downcase.split(/[^[[:word:]]]+/)).length}].flatten}
dataset = CSV.open("inner_altright_machine_learning_dataset_train2.csv", "w")
sample_altright_counts.each do |row|
  dataset << row
end
sample_background_counts.each do |row|
  dataset << row
end
dataset.close
