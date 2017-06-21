load '/media/dgaff/backup/Code/reddit_random_walk/code/extensions/array.rb'
require 'csv'
filepath = `git rev-parse --show-toplevel`.strip
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
`ls #{filepath}/baumgartner_data/comments_altrighters/`.split("\n").each do |file|
  puts file
  begin
    background_file = CSV.read("#{filepath}/baumgartner_data/comments_background/#{file}");false
    altright = background_file.select{|x| x[1] == "altright"};false
    altright.collect(&:last).collect(&:downcase).collect{|s| s.split(/[^[[:word:]]]+/)}.flatten.counts.each do |word, count|
      altright_counts[word] ||= 0
      altright_counts[word] += count
    end
  rescue
    next
  end
end;false
background_sum = background_counts.values.sum
altright_sum = altright_counts.values.sum
representativeness = Hash[altright_counts.collect{|k,v| [k, (v/altright_sum.to_f)/((background_counts[k]||1)/background_sum)]}];false
altright_comments = []
`ls #{filepath}/baumgartner_data/comments_altrighters/`.split("\n").each do |file|
  puts file
  begin
    background_file = CSV.read("#{filepath}/baumgartner_data/comments_altrighters/#{file}");false
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

top_terms_altright = representativeness.select{|k,v| v > 1 && (background_counts[k]||0)/background_sum > 0.00001}.sort_by{|k,v| v}.reverse.collect(&:first);false
top_terms_background = representativeness.select{|k,v| v < 1 && (background_counts[k]||0)/background_sum > 0.00001}.sort_by{|k,v| v}.collect(&:first);false

terms = top_terms_altright|top_terms_background;false
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
