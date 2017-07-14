require 'csv'
filepath = `git rev-parse --show-toplevel`.strip
load filepath+'/commands/array.rb'
FILEPATH = filepath
class GenerateKeywordGroups
  def full_comments_altright(prefix="")
    return @full_comments_altright if @full_comments_altright
    @full_comments_altright = []
    `ls #{FILEPATH}/baumgartner_data#{prefix}/comments_altright/`.split("\n").each do |file|
      puts file
      begin
        CSV.read("#{FILEPATH}/baumgartner_data#{prefix}/comments_altright/#{file}", col_sep: ",", row_sep: "\n").each do |row|
          @full_comments_altright << row
        end
      rescue
        next
      end
    end
  end

  def altright_comments_altright(prefix="")
    return @altright_comments_altright if @altright_comments_altright
    full_comments_altright;false
    @altright_comments_altright = @full_comments_altright.select{|c| c[1] == "altright"}
  end

  def background_comments_altright
    return @background_comments_altright if @background_comments_altright
    full_comments_altright;false
    @background_comments_altright = @full_comments_altright.select{|c| c[1] != "altright"}.shuffle.first(@altright_comments_altright.length*2);false
  end

  def background_comments
    return @background_comments if @background_comments
    altright_comments_altright;false
    @background_comments = []
    `ls #{FILEPATH}/baumgartner_data#{prefix}/comments_background/`.split("\n").each do |file|
      puts file
      begin
        CSV.read("#{FILEPATH}/baumgartner_data#{prefix}/comments_background/#{file}", col_sep: ",", row_sep: "\n").each do |row|
          @background_comments << row
        end
      rescue
        next
      end
    end
    @background_comments = @background_comments.shuffle.first(@altright_comments_altright.length*2)#sample a small amount just because the corpus is so gigantic
  end

  def generate_keywords(positive_corpus, negative_corpus, outfile)
    positive_counts = {}
    positive_corpus.each do |comment|
      comment.last.downcase.split(/[^[[:word:]]]+/).counts.reject{|k,v| k.empty?}.each do |word, count|
        positive_counts[word] ||= 0
        positive_counts[word] += count
      end
    end;false
    negative_counts = {}
    negative_corpus.each do |comment|
      comment.last.downcase.split(/[^[[:word:]]]+/).counts.reject{|k,v| k.empty?}.each do |word, count|
        negative_counts[word] ||= 0
        negative_counts[word] += count
      end
    end;false
    positive_sum = positive_counts.values.sum
    negative_sum = negative_counts.values.sum
    representativeness = Hash[positive_counts.collect{|k,v| [k, (v/positive_sum.to_f)/((negative_counts[k]||1)/negative_sum)]}];false
    top_rare_terms_positive = representativeness.select{|k,v| v > 2 && (negative_counts[k]||0)/negative_sum > 0.0001}.sort_by{|k,v| v}.reverse.collect(&:first);false
    top_terms_positive = representativeness.select{|k,v| v > 1 && (positive_counts[k]||0)/positive_sum > 0.001}.sort_by{|k,v| v}.reverse.collect(&:first);false
    top_terms_negative = representativeness.select{|k,v| v < 1 && (negative_counts[k]||0)/negative_sum > 0.0001}.sort_by{|k,v| v}.collect(&:first);false
    rare_positive_only = representativeness.select{|k,v| v > 1 && (negative_counts[k]||0)/negative_sum < 0.0001}.sort_by{|k,v| v}.reverse.collect(&:first);false
    gapness = Hash[positive_counts.collect{|k,v| [k, (v/positive_sum.to_f)-((negative_counts[k]||1)/negative_sum)]}];false
    terms = top_terms_positive|top_terms_negative;false
    keyword_groups = [
    representativeness.select{|k,v| v > 2}.keys,
    representativeness.select{|k,v| v > 1 && positive_counts[k] > 100}.keys,
    representativeness.select{|k,v| v > 2 && (negative_counts[k]||0)/negative_sum < 0.0001}.keys,
    representativeness.select{|k,v| v > 2 && (negative_counts[k]||0)/negative_sum > 0.0001}.keys,
    gapness.select{|k,v| v > 0}.keys,
    gapness.select{|k,v| v > 1.6625465251303116e-07}.keys,
    gapness.select{|k,v| v > 0 && (negative_counts[k]||0)/negative_sum < 0.0001}.keys,
    positive_counts.sort_by{|k,v| v}.reverse.first(100).collect(&:first) - negative_counts.sort_by{|k,v| v}.reverse.first(100).collect(&:first),
    positive_counts.sort_by{|k,v| v}.reverse.first(1000).collect(&:first) - negative_counts.sort_by{|k,v| v}.reverse.first(1000).collect(&:first),
    representativeness.select{|k,v| v < 0.5}.keys,
    representativeness.select{|k,v| v < 1 && negative_counts[k] > 100}.keys,
    representativeness.select{|k,v| v < 0.5 && (negative_counts[k]||0)/negative_sum > 0.0001}.keys,
    representativeness.select{|k,v| v < 0.5 && (positive_counts[k]||0)/positive_sum > 0.0001}.keys,
    gapness.select{|k,v| v < 0}.keys,
    gapness.select{|k,v| v < -1.199021482828853e-06}.keys,
    gapness.select{|k,v| v < 0 && (negative_counts[k]||0)/negative_sum > 0.0001}.keys,
    negative_counts.sort_by{|k,v| v}.reverse.first(100).collect(&:first) - positive_counts.sort_by{|k,v| v}.reverse.first(100).collect(&:first),
    negative_counts.sort_by{|k,v| v}.reverse.first(1000).collect(&:first) - positive_counts.sort_by{|k,v| v}.reverse.first(1000).collect(&:first)];false
    outfile.write(keyword_groups.to_json)
    outfile.close
  end
  
  def run
    altright_comments_altright
    background_comments
    `mkdir #{FILEPATH}/baumgartner_data/machine_learning_resources`
    `mkdir #{FILEPATH}/baumgartner_data/machine_learning_trials`
    `mkdir #{FILEPATH}/baumgartner_data/machine_learning_results`
    generate_keywords(@altright_comments_altright, @background_comments_altright, File.open("#{FILEPATH}/baumgartner_data/machine_learning_resources/inner_keyword_groups.json", "w"))
    generate_keywords(@altright_comments_altright, @background_comments, File.open("#{FILEPATH}/baumgartner_data/machine_learning_resources/background_keyword_groups.json", "w"))
    inner_csv = CSV.open("#{FILEPATH}/baumgartner_data/machine_learning_resources/inner_dataset.csv", "w")
    background_csv = CSV.open("#{FILEPATH}/baumgartner_data/machine_learning_resources/background_dataset.csv", "w")
    @altright_comments_altright.each do |comment|
      inner_csv << [comment, 1.0].flatten
      background_csv << [comment, 1.0].flatten
    end;false
    @background_comments_altright.each do |comment|
      inner_csv << [comment, 0.0].flatten
    end;false
    @background_comments.each do |comment|
      background_csv << [comment, 0.0].flatten
    end;false
    inner_csv.close
    background_csv.close
  end
  
  def run_test
    altright_comments_altright
    background_comments
    `mkdir #{FILEPATH}/baumgartner_data_test/machine_learning_resources`
    `mkdir #{FILEPATH}/baumgartner_data_test/machine_learning_trials`
    `mkdir #{FILEPATH}/baumgartner_data_test/machine_learning_results`
    generate_keywords(@altright_comments_altright, @background_comments_altright, File.open("#{FILEPATH}/baumgartner_data_test/machine_learning_resources/inner_keyword_groups.json", "w"))
    generate_keywords(@altright_comments_altright, @background_comments, File.open("#{FILEPATH}/baumgartner_data_test/machine_learning_resources/background_keyword_groups.json", "w"))
    inner_csv = CSV.open("#{FILEPATH}/baumgartner_data_test/machine_learning_resources/inner_dataset.csv", "w")
    background_csv = CSV.open("#{FILEPATH}/baumgartner_data_test/machine_learning_resources/background_dataset.csv", "w")
    @altright_comments_altright.each do |comment|
      inner_csv << [comment, 1.0].flatten
      background_csv << [comment, 1.0].flatten
    end
    @background_comments_altright.each do |comment|
      inner_csv << [comment, 0.0].flatten
    end
    @background_comments.each do |comment|
      background_csv << [comment, 0.0].flatten
    end
    inner_csv.close
    background_csv.close
  end
end

if $0 == __FILE__ && ARGV.empty?
  GenerateKeywordGroups.run
elsif $0 == __FILE__ && ARGV[0] == "test"
  GenerateKeywordGroups.run_test 
end
