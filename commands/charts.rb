filepath = `git rev-parse --show-toplevel`.strip
load filepath+'/array.rb'
require 'csv'
require 'json'
FILEPATH = filepath
class Charts
  def all_comments
    return @all_altright_comments if @all_altright_comments
    @all_altright_comments = []
    `ls #{FILEPATH}/baumgartner_data/comments_altright/`.split("\n").each do |file|
      puts file
      begin
        background_file = CSV.read("#{FILEPATH}/baumgartner_data/comments_altright/#{file}", col_sep: ",", row_sep: "\n");false
        background_file.each do |row|
        @all_altright_comments << row
        end
      rescue
        next
      end
    end;false
  end

  def all_submissions
    return @all_altright_submissions if @all_altright_submissions
    @all_altright_submissions = []
    `ls #{FILEPATH}/baumgartner_data/submissions_altright/`.split("\n").each do |file|
      puts file
      begin
        background_file = CSV.read("#{FILEPATH}/baumgartner_data/submissions_altright/#{file}", col_sep: ",", row_sep: "\n");false
        background_file.each do |row|
        @all_altright_submissions << row
        end
      rescue
        next
      end
    end;false
  end

  def cohorts
    return @cohorts if @cohorts
    @cohorts = {}
    @all_altright_submissions.each do |r|
      if @cohorts[r[2]].nil? || @cohorts[r[2]].to_i > Time.at(r[0].to_i).strftime("%Y").to_i
        @cohorts[r[2]] = Time.at(r[0].to_i).strftime("%Y")
      end
    end;false
    @all_altright_comments.each do |r|
      if @cohorts[r[2]].nil? || @cohorts[r[2]].to_i > Time.at(r[0].to_i).strftime("%Y").to_i
        @cohorts[r[2]] = Time.at(r[0].to_i).strftime("%Y")
      end
    end;false
    @cohorts_by_year = {}
    @cohorts.collect{|k,v| @cohorts_by_year[v] ||= []; @cohorts_by_year[v] << k};false
    @cohorts_by_year;false
  end

  def cohorts_daily
    return @cohorts_daily if @cohorts_daily
    @cohorts_daily = {}
    @cohorts_daily_submissions = {}
    @cohorts_daily_comments = {}
    @all_altright_submissions.each do |r|
      if @cohorts_daily[r[2]].nil? || @cohorts_daily[r[2]].to_i > Time.at(r[0].to_i).strftime("%Y").to_i
        @cohorts_daily[r[2]] = Time.at(r[0].to_i).strftime("%Y")
        @cohorts_daily_submissions[r[2]] = Time.at(r[0].to_i).strftime("%Y")
      end
    end;false
    @all_altright_comments.each do |r|
      if @cohorts_daily[r[2]].nil? || @cohorts_daily[r[2]].to_i > Time.at(r[0].to_i).strftime("%Y").to_i
        @cohorts_daily[r[2]] = Time.at(r[0].to_i).strftime("%Y")
        @cohorts_daily_comments[r[2]] = Time.at(r[0].to_i).strftime("%Y")
      end
    end;false
    @cohorts_by_day = {}
    @cohorts_daily.collect{|k,v| @cohorts_by_day[v] ||= []; @cohorts_by_day[v] << k};false
    @cohorts_by_day;false
  end

  def first_day
    return @first_day if @first_day
    @first_day = Time.at([@all_altright_comments.sort_by{|k| k.first.to_i}.first.first.to_i, @all_altright_submissions.sort_by{|k| k.first.to_i}.first.first.to_i].sort.first)
  end

  def first_altright_day
    return @first_altright_day if @first_altright_day
    @first_altright_day = Time.at([@all_altright_comments.select{|k| k[1] == "altright"}.sort_by{|k| k.first.to_i}.first.first.to_i, @all_altright_submissions.select{|k| k[1] == "altright"}.sort_by{|k| k.first.to_i}.first.first.to_i].sort.first)
  end

  def last_day
    return @last_day if @last_day
    @last_day = Time.at([@all_altright_comments.sort_by{|k| k.first.to_i}.last.first.to_i, @all_altright_submissions.sort_by{|k| k.first.to_i}.last.first.to_i].sort.last)
  end

  def last_altright_day
    return @last_altright_day if @last_altright_day
    @last_altright_day = Time.at([@all_altright_comments.select{|k| k[1] == "altright"}.sort_by{|k| k.first.to_i}.last.first.to_i, @all_altright_submissions.select{|k| k[1] == "altright"}.sort_by{|k| k.first.to_i}.last.first.to_i].sort.last)
  end

  def daily_comment_counts
    return @daily_altright_comment_counts_reddit if @daily_altright_comment_counts_reddit
    @daily_altright_comment_counts_reddit = {}
    @cohort_daily_altright_comment_counts_reddit = {}
    @all_altright_comments.each do |comment|
      @daily_altright_comment_counts_reddit[Time.at(comment[0].to_i).strftime("%Y-%m-%d")] ||= 0
      @daily_altright_comment_counts_reddit[Time.at(comment[0].to_i).strftime("%Y-%m-%d")] += 1
      @cohort_daily_altright_comment_counts_reddit[@cohorts[comment[2]]] ||= {}
      @cohort_daily_altright_comment_counts_reddit[@cohorts[comment[2]]][Time.at(comment[0].to_i).strftime("%Y-%m-%d")] ||= 0
      @cohort_daily_altright_comment_counts_reddit[@cohorts[comment[2]]][Time.at(comment[0].to_i).strftime("%Y-%m-%d")] += 1
    end;false
  end
  
  def daily_submission_counts
    return @daily_altright_submission_counts_reddit if @daily_altright_submission_counts_reddit
    @daily_altright_submission_counts_reddit = {}
    @cohort_daily_altright_submission_counts_reddit = {}
    @all_altright_submissions.each do |submission|
      @daily_altright_submission_counts_reddit[Time.at(submission[0].to_i).strftime("%Y-%m-%d")] ||= 0
      @daily_altright_submission_counts_reddit[Time.at(submission[0].to_i).strftime("%Y-%m-%d")] += 1
      @cohort_daily_altright_submission_counts_reddit[@cohorts[comment[2]]] ||= {}
      @cohort_daily_altright_submission_counts_reddit[@cohorts[comment[2]]][Time.at(comment[0].to_i).strftime("%Y-%m-%d")] ||= 0
      @cohort_daily_altright_submission_counts_reddit[@cohorts[comment[2]]][Time.at(comment[0].to_i).strftime("%Y-%m-%d")] += 1
    end;false
  end

  def daily_altright_comment_counts
    return @daily_altright_comment_counts if @daily_altright_comment_counts
    @daily_altright_comment_counts = {}
    @cohort_daily_altright_comment_counts = {}
    @all_altright_comments.each do |comment|
      next if comment[1] != "altright"
      @daily_altright_comment_counts[Time.at(comment[0].to_i).strftime("%Y-%m-%d")] ||= 0
      @daily_altright_comment_counts[Time.at(comment[0].to_i).strftime("%Y-%m-%d")] += 1
      @cohort_daily_altright_comment_counts[@cohorts[comment[2]]] ||= {}
      @cohort_daily_altright_comment_counts[@cohorts[comment[2]]][Time.at(comment[0].to_i).strftime("%Y-%m-%d")] ||= 0
      @cohort_daily_altright_comment_counts[@cohorts[comment[2]]][Time.at(comment[0].to_i).strftime("%Y-%m-%d")] += 1
    end;false
  end
  
  def daily_altright_submission_counts
    return @daily_altright_submission_counts_reddit if @daily_altright_submission_counts_reddit
    @daily_altright_submission_counts_reddit = {}
    @cohort_daily_altright_submission_counts_reddit = {}
    @all_altright_submissions.each do |submission|
      next if submission[1] != "altright"
      @daily_altright_submission_counts_reddit[Time.at(submission[0].to_i).strftime("%Y-%m-%d")] ||= 0
      @daily_altright_submission_counts_reddit[Time.at(submission[0].to_i).strftime("%Y-%m-%d")] += 1
      @cohort_daily_altright_submission_counts_reddit[@cohorts[comment[2]]] ||= {}
      @cohort_daily_altright_submission_counts_reddit[@cohorts[comment[2]]][Time.at(comment[0].to_i).strftime("%Y-%m-%d")] ||= 0
      @cohort_daily_altright_submission_counts_reddit[@cohorts[comment[2]]][Time.at(comment[0].to_i).strftime("%Y-%m-%d")] += 1
    end;false
  end

  def chart_daily_comments_by_altright_on_reddit
    dataset = [["Day", "All Altrighters", @cohorts_by_year.keys.collect{|y| y+" Cohort"}]]
    (@first_day.to_date..@last_day.to_date).each do |day|
      dataset << [day.to_s, @daily_altright_comment_counts_reddit[day.to_s]||0, @cohorts_by_year.keys.collect{|y| @cohort_daily_altright_comment_counts_reddit[y][day.to_s] || 0}].flatten
    end;false
    write_tabular(dataset, __method__.to_s, "Daily counts of comments generated by all users who Submitted or Commented at least once on /r/altright")
  end

  def chart_cumulative_daily_comments_by_altright_on_reddit
    dataset = [["Day", "All Altrighters", @cohorts_by_year.keys.collect{|y| y+" Cohort"}]]
    cur_count = 0
    cohort_count = Hash[@cohorts_by_year.keys.collect{|y| [y, 0]}]
    total_count = @daily_altright_comment_counts_reddit.values.sum
    (@first_day.to_date..@last_day.to_date).each do |day|
      cur_count += @daily_altright_comment_counts_reddit[day.to_s]||0
      dataset << [day.to_s, cur_count, @cohorts_by_year.keys.collect{|y| cohort_count[y] += @cohort_daily_altright_comment_counts_reddit[y][day.to_s] || 0; cohort_count[y]}].flatten
    end;false
    write_tabular(dataset, __method__.to_s, "Cumulative daily counts of comments generated by all users who Submitted or Commented at least once on /r/altright")
  end

  def chart_daily_comments_in_altright
    dataset = [["Day", "All Altrighters", @cohorts_by_year.keys.collect{|y| y+" Cohort"}]]
    (@first_day.to_date..@last_day.to_date).each do |day|
      dataset << [day.to_s, @daily_altright_comment_counts[day.to_s]||0, @cohorts_by_year.keys.collect{|y| @cohort_daily_altright_comment_counts[y][day.to_s] || 0}].flatten
    end;false
    write_tabular(dataset, __method__.to_s, "Daily counts of comments generated by all users who Submitted or Commented at least once on /r/altright, restricted to their posts on the altright subreddit")
  end

  def chart_cumulative_daily_comments_in_altright
    dataset = [["Day", "All Altrighters", @cohorts_by_year.keys.collect{|y| y+" Cohort"}]]
    cur_count = 0
    cohort_count = Hash[@cohorts_by_year.keys.collect{|y| [y, 0]}]
    total_count = @daily_altright_comment_counts_reddit.values.sum
    (@first_day.to_date..@last_day.to_date).each do |day|
      cur_count += @daily_altright_comment_counts_reddit[day.to_s]||0
      dataset << [day.to_s, cur_count, @cohorts_by_year.keys.collect{|y| cohort_count[y] += @cohort_daily_altright_comment_counts_reddit[y][day.to_s] || 0; cohort_count[y]}].flatten
    end;false
    write_tabular(dataset, __method__.to_s, "Cumulative daily counts of comments generated by all users who Submitted or Commented at least once on /r/altright, restricted to their posts on the altright subreddit")
  end
  
  def generate_user_datasheet
    cohorts_daily
    comments_by_users = {}
    submissions_by_users = {} 
    posts_by_users = {}
    @all_altright_comments.collect{|r| comments_by_users[r[2]] ||= []; comments_by_users[r[2]] << r; posts_by_users[r[2]] ||= []; posts_by_users[r[2]] << r};false
    @all_altright_submissions.collect{|r| submissions_by_users[r[2]] ||= []; submissions_by_users[r[2]] << r; posts_by_users[r[2]] ||= []; posts_by_users[r[2]] << r};false
    dataset = [
      "Screen Name", 
      "Comment Count", 
      "Submission Count", 
      "Post Count",
      "Altright Comment Count", 
      "Altright Submission Count", 
      "Altright Post Count",
      "Altright Is Modal Comments",
      "Altright Is Modal Submissions",
      "Altright Is Modal Posts",
      "Cohort Year",
      "Age In Days",
      ""
      ]
  end
  def write_tabular(dataset, method, description)
    csv = CSV.open("#{FILEPATH}/paper/charts/raw/#{method.to_s}.csv", "w")
    f = File.open("#{FILEPATH}/paper/charts/description/#{method.to_s}.txt", "w")
    dataset.each do |row|
      csv << row
    end;false
    csv.close
    f.write(description)
    f.close
  end

  def self.generate_chart_datasets
    instance = self.new
    (self.methods-Class.methods).each do |method|
      instance.send(method)
    end
  end
end