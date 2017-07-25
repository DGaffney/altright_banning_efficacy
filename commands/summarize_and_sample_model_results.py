import copy
import numpy as np
import json
import csv
import json
import os
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", help="dataset to sanitize ('background' or 'inner')")
ap.add_argument("-t", "--test", help="is test? Add in option if it's a test otherwise leave empty")
ap.add_argument("-c", "--count", help="number of workers that were used - default is 10", type=int, default=10)
args = vars(ap.parse_args())
dataset = args["dataset"]
prefix = '' if args["test"] == None else '_test'
filepath = os.popen('git rev-parse --show-toplevel').read().strip()
path = filepath+"/baumgartner_data"+prefix+"/machine_learning_resources"
results_path = filepath+"/baumgartner_data"+prefix+"/machine_learning_results"
models_used =  os.popen("ls "+path+"/"+dataset+"_neural_net_voter_*").read().split("\n")[:args["count"]]
def read_csv_str(filename):
  dataset = []
  i = 0
  with open(filename, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        dataset.append(row)
  return dataset

datafiles = sorted(list(set(["missing_comments.csv"]).union(set([r.split("_")[-1] for r in os.popen("ls "+results_path).read().split("\n")]))-set(['', 'comments.csv'])))
all_data = {}
for month in datafiles:
  print month
  all_data[month] = [r[:-1] for r in read_csv_str(results_path+"/"+os.popen("ls "+results_path+" | grep "+month).read().split("\n")[0])]

model_results = []
for i,model_used in enumerate(models_used):
  model_result = []
  print i
  for month in datafiles:
    print "\t"+month
    if month == "missing_comments.csv":
      model_result.append([float(r[-1]) for r in read_csv_str(results_path+"/"+"dataset_"+dataset+"_model_"+str(i)+"_"+month)])
    else:
      model_result.append([float(r[-1]) for r in read_csv_str(results_path+"/"+"dataset_"+dataset+"_model_"+str(i)+"_RC_"+month)])
  model_results.append(model_result)

maj_votes = []
avg_votes = []
for month_iter,file in enumerate(datafiles):
  print file
  maj_votes.append(np.mean(np.round(np.array([r[month_iter] for r in model_results]).transpose()), 1))
  avg_votes.append(np.mean(np.array([r[month_iter] for r in model_results]).transpose(), 1))

sampled = {}
aggregated_results_path = filepath+"/baumgartner_data"+prefix+"/machine_learning_results_aggregated/"
for month_iter,month in enumerate(datafiles):
  print month
  rows_to_write = []
  for row_iter,row in enumerate(all_data[month]):
    result_row = copy.deepcopy(row)
    result_row.append(maj_votes[month_iter][row_iter])
    result_row.append(avg_votes[month_iter][row_iter])
    if np.random.random() < 1.1764705882352942e-04 and result_row[1] != "altright" or result_row[1] == "altright" and np.random.random() < 0.006666666666666667:
      if month not in sampled.keys():
        sampled[month] = []
      sampled[month].append(result_row)
    rows_to_write.append(result_row)
  with open(aggregated_results_path+"dataset_"+args['dataset']+"_count_"+str(args["count"])+"_"+month, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(rows_to_write)

sampleset = []
for month in sampled.keys():
  for row in sampled[month]:
    new_row = copy.deepcopy(row)
    new_row[5] = new_row[5].replace("\n", " ")
    new_row.append(month)
    sampleset.append(new_row)

np.random.shuffle(sampleset)
with open(aggregated_results_path+"dataset_"+args['dataset']+"_count_"+str(args["count"])+"_validation_sample.csv", 'wb') as f:
  writer = csv.writer(f)
  writer.writerows(sampleset)