require 'csv'
filepath = `git rev-parse --show-toplevel`.strip
altright_accounts = []
`ls #{filepath}/baumgartner_data/comments_altrighters`.split("\n").each do |file|
  altright_accounts << CSV.read("#{filepath}/baumgartner_data/comments_altrighters/#{file}").collect{|x| x[2]}
end
`ls #{filepath}/baumgartner_data/submissions_altrighters`.split("\n").each do |file|
  altright_accounts << CSV.read("#{filepath}/baumgartner_data/submissions_altrighters/#{file}").collect{|x| x[2]}
end
all_accounts = altright_accounts.flatten.uniq
csv = CSV.open("#{filepath}/baumgartner_data/altrighters.csv", "w")
all_accounts.collect{|a| csv << [a]};false
csv.close
