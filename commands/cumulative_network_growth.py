import numpy as np
import random
import igraph
import string
import re
import json
import pickle
import csv
import argparse
import os
from os import listdir
from os.path import isfile, join
filepath = os.popen('git rev-parse --show-toplevel').read().strip()
graph = igraph.Graph()
graph.add_vertex()
graph.vs()[0]['name'] = "reddit.com"
files = os.popen('ls '+filepath+"/../dissertation_agent_based/Sandbox/larger_data/edge_creation/").read().strip().split("\n")
edge_creation_filepath = filepath+"/../dissertation_agent_based/Sandbox/larger_data/edge_creation/"
daily_altright_densities = json.loads(open("/media/dgaff/backup/Code/altright_banning_efficacy/baumgartner_data/daily_altright_densities.json").read())
daily_altright_miss_densities = json.loads(open("/media/dgaff/backup/Code/altright_banning_efficacy/baumgartner_data/daily_altright_miss_densities.json").read())
def read_csv_str(filename):
  dataset = []
  i = 0
  with open(filename, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        dataset.append(row)
  return dataset

preloaded_edges = []
for f in files[0:3765]:
  print f
  for row in read_csv_str(edge_creation_filepath+f):
    preloaded_edges.append(row)

nodes = list(set([item for sublist in preloaded_edges for item in sublist]))
graph = igraph.Graph(directed=True)
graph.add_vertices(nodes)
graph.add_edges(preloaded_edges)
  # new_edges = read_csv_str(edge_creation_filepath+f)
  # for edge in new_edges:
  #   if len(graph.vs.select(name_eq=edge[0])) == 0:
  #     graph.add_vertex(edge[0])
  #   if len(graph.vs.select(name_eq=edge[1])) == 0:
  #     graph.add_vertex(edge[1])
  #   graph.add_edges([(edge[0], edge[1])])
dataset = []
for f in files[4009:]:
  print f
  edge_count = len(graph.es)
  node_count = len(graph.vs)
  new_edges = read_csv_str(edge_creation_filepath+f)
  existing_nodes = set(graph.vs()['name'])
  new_nodes = set([item for sublist in new_edges for item in sublist])-existing_nodes
  graph.add_vertices(list(new_nodes))
  graph.add_edges(new_edges)
  altright_node = graph.vs.select(name_eq="altright")[0]
  degree = altright_node.degree()
  indegree = altright_node.indegree()
  outdegree = altright_node.outdegree()
  #first_clustering = graph.transitivity_local_undirected([altright_node])[0]
  #first_pagerank = graph.personalized_pagerank([altright_node])[0]
  #first_constraint = graph.constraint([altright_node])[0]
  altright_neighbors = list(set([v['name'] for v in altright_node.neighbors()]))
  if f in daily_altright_densities.keys() and f in daily_altright_miss_densities.keys():
    for alter_name in list(set(daily_altright_densities[f].keys()).intersection(set(daily_altright_miss_densities[f].keys()))):
      if random.random() < 100.0/len(daily_altright_densities[f].keys()):
        print alter_name
        alter_node = graph.vs.select(name_eq=alter_name)[0]
        alter_degree = alter_node.degree()
        alter_indegree = alter_node.indegree()
        alter_outdegree = alter_node.outdegree()
        alter_neighbors = [v['name'] for v in alter_node.neighbors()]
        #altright_distance = graph.shortest_paths_dijkstra(source=alter_name, target="altright")[0][0]
        #alter_distance = graph.shortest_paths_dijkstra(source="altright", target=alter_name)[0][0]
        jaccard = graph.similarity_jaccard(["altright", alter_name])[0][1]
        dice = graph.similarity_dice(["altright", alter_name])[0][1]
        #invlogweighted = graph.similarity_inverse_log_weighted(["altright", alter_name])[0][1]
        #maxflow = graph.maxflow(altright_node.index, alter_node.index)
        #mincut = graph.mincut_value(altright_node.index, alter_node.index)
        #second_clustering = graph.transitivity_local_undirected([alter_node])[0]
        #average_clustering = sum([first_clustering, second_clustering])/2
        #second_pagerank = graph.personalized_pagerank([alter_node])[0]
        #average_pagerank = sum([first_pagerank, second_pagerank])/2
        #second_constraint = graph.constraint([alter_node])[0]
        #average_constraint = sum([first_constraint, second_constraint])/2
        common_neighbors = len(set(altright_neighbors)&set(alter_neighbors))
        intensity = float(daily_altright_densities[f][alter_name])/(daily_altright_densities[f][alter_name]+daily_altright_miss_densities[f][alter_name])
        miss_count = daily_altright_miss_densities[f][alter_name]
        #dataset.append([f, alter_name, daily_altright_densities[f][alter_name], degree, indegree, outdegree, first_clustering, alter_degree, alter_indegree, alter_outdegree, second_clustering, average_clustering, jaccard, dice, common_neighbors, edge_count, node_count])
        dataset.append([f, alter_name, daily_altright_densities[f][alter_name], miss_count, intensity, degree, indegree, outdegree, alter_degree, alter_indegree, alter_outdegree, jaccard, dice, common_neighbors, edge_count, node_count])

addendum = [['2015-10-14', u'badeconomics', 2, 1, 0.6666666666666666, 11, 6, 5, 4901, 2446, 2455, 0.0025015634771732333, 0.004990642545227698, 8, 34445156, 396515], ['2015-10-14', u'relationships', 1, 20, 0.047619047619047616, 11, 6, 5, 38019, 19056, 18963, 0.0003772319557381172, 0.0007541794109020824, 9, 34445156, 396515], ['2015-10-14', u'BestOfOutrageCulture', 2, 1, 0.6666666666666666, 11, 6, 5, 5321, 2656, 2665, 0.0022740193291642978, 0.004537719795802609, 8, 34445156, 396515], ['2015-10-14', u'edmprodcirclejerk', 1, 2, 0.3333333333333333, 11, 6, 5, 5418, 2705, 2713, 0.0022166805209199226, 0.004423555432679017, 8, 34445156, 396515], ['2015-10-14', u'Jokes', 1, 8, 0.1111111111111111, 11, 6, 5, 36847, 18522, 18325, 0.00033015558581981757, 0.0006600932381698915, 8, 34445156, 396515], ['2015-10-14', u'WhiteRights', 6, 3, 0.6666666666666666, 11, 6, 5, 6358, 3197, 3161, 0.0018975332068311196, 0.0037878787878787876, 8, 34445156, 396515], ['2015-10-14', u'nba', 10, 44, 0.18518518518518517, 11, 6, 5, 45272, 22772, 22500, 0.00032181935207037116, 0.0006434316353887399, 9, 34445156, 396515], ['2015-10-14', u'Boise', 8, 1, 0.8888888888888888, 11, 6, 5, 7182, 3579, 3603, 0.0012970168612191958, 0.0025906735751295338, 6, 34445156, 396515], ['2015-10-14', u'mindcrack', 1, 1, 0.5, 11, 6, 5, 22693, 11357, 11336, 0.0006258257422988666, 0.001250868658790827, 9, 34445156, 396515], ['2015-10-14', u'DotA2', 7, 66, 0.0958904109589041, 11, 6, 5, 49438, 24904, 24534, 0.0002962865420068475, 0.00059239756458779, 9, 34445156, 396515], ['2015-10-14', u'instant_regret', 1, 7, 0.125, 11, 6, 5, 11788, 5901, 5887, 0.0008937691521961185, 0.0017859420844495472, 7, 34445156, 396515], ['2015-10-14', u'Catholicism', 7, 1, 0.875, 11, 6, 5, 15460, 7771, 7689, 0.0008234688625836336, 0.0016455826391031574, 8, 34445156, 396515], ['2015-10-14', u'confession', 1, 4, 0.2, 11, 6, 5, 22221, 11094, 11127, 0.0005608524957936063, 0.0011210762331838565, 8, 34445156, 396515], ['2015-10-14', u'Firearms', 1, 2, 0.3333333333333333, 11, 6, 5, 13291, 6621, 6670, 0.0009418412997409936, 0.0018819101387908726, 8, 34445156, 396515], ['2015-10-14', u'FifaCareers', 1, 3, 0.25, 11, 6, 5, 7963, 3980, 3983, 0.0013809429867824028, 0.0027580772261623326, 7, 34445156, 396515], ['2015-10-14', u'MMA', 4, 25, 0.13793103448275862, 11, 6, 5, 31289, 15800, 15489, 0.0004671441918405481, 0.0009338521400778211, 9, 34445156, 396515], ['2015-10-14', u'MURICA', 2, 4, 0.3333333333333333, 11, 6, 5, 23762, 11858, 11904, 0.000516896039284099, 0.0010332579916047789, 8, 34445156, 396515], ['2015-10-14', u'travel', 1, 3, 0.25, 11, 6, 5, 30544, 15285, 15259, 0.00040669005134461896, 0.000813049443569287, 8, 34445156, 396515], ['2015-10-14', u'babyelephantgifs', 1, 1, 0.5, 11, 6, 5, 5364, 2668, 2696, 0.0018975332068311196, 0.0037878787878787876, 7, 34445156, 396515], ['2015-10-14', u'economy', 1, 3, 0.25, 11, 6, 5, 12848, 6421, 6427, 0.0009513616363420145, 0.0019009148152548416, 8, 34445156, 396515], ['2015-10-14', u'askscience', 3, 2, 0.6, 11, 6, 5, 40041, 19944, 20097, 0.0003064312253418623, 0.0006126747080222094, 8, 34445156, 396515], ['2015-10-14', u'MensLib', 1, 1, 0.5, 11, 6, 5, 2653, 1337, 1316, 0.003863134657836645, 0.007696536558548654, 7, 34445156, 396515], ['2015-10-14', u'justneckbeardthings', 3, 7, 0.3, 11, 6, 5, 19197, 9611, 9586, 0.0006458383789456688, 0.001290843081887858, 8, 34445156, 396515], ['2015-10-14', u'occult', 2, 2, 0.5, 11, 6, 5, 11885, 5994, 5891, 0.0010568031704095112, 0.002111375032990235, 8, 34445156, 396515], ['2015-10-14', u'MHOC', 1, 1, 0.5, 11, 6, 5, 4367, 2221, 2146, 0.0028439388553146107, 0.005671747607231478, 8, 34445156, 396515], ['2015-10-14', u'TwoXChromosomes', 6, 4, 0.6, 11, 6, 5, 37665, 18836, 18829, 0.00033582402820921836, 0.0006714225765841376, 8, 34445156, 396515], ['2015-10-14', u'medicine', 2, 1, 0.6666666666666666, 11, 6, 5, 13996, 6939, 7057, 0.00088261253309797, 0.001763668430335097, 8, 34445156, 396515], ['2015-10-14', u'Borderlands', 1, 4, 0.2, 11, 6, 5, 18037, 9024, 9013, 0.0006985679357317499, 0.0013961605584642235, 8, 34445156, 396515], ['2015-10-14', u'patientgamers', 4, 6, 0.4, 11, 6, 5, 18304, 9173, 9131, 0.0006790018672551349, 0.0013570822731128074, 8, 34445156, 396515], ['2015-10-14', u'rant', 1, 1, 0.5, 11, 6, 5, 13837, 6941, 6896, 0.000887705281846427, 0.0017738359201773838, 8, 34445156, 396515], ['2015-10-14', u'worldpolitics', 30, 14, 0.6818181818181818, 11, 6, 5, 20366, 10167, 10199, 0.0006050979502306936, 0.0012094640562400785, 8, 34445156, 396515], ['2015-10-14', u'leafs', 2, 5, 0.2857142857142857, 11, 6, 5, 11509, 5748, 5761, 0.0009653840849537994, 0.0019289060347203086, 7, 34445156, 396515], ['2015-10-14', u'Games', 1, 5, 0.16666666666666666, 11, 6, 5, 49032, 24610, 24422, 0.00028669724770642203, 0.0005732301519059903, 9, 34445156, 396515], ['2015-10-14', u'PoliticalDiscussion', 23, 13, 0.6388888888888888, 11, 6, 5, 20252, 10132, 10120, 0.0006320113762047717, 0.0012632243802305383, 8, 34445156, 396515], ['2015-10-14', u'bodybuilding', 2, 6, 0.25, 11, 6, 5, 22052, 11018, 11034, 0.0005770756690471038, 0.0011534856895681637, 8, 34445156, 396515], ['2015-10-14', u'Torontobluejays', 4, 38, 0.09523809523809523, 11, 6, 5, 10827, 5537, 5290, 0.0010196649672250546, 0.002037252619324796, 7, 34445156, 396515], ['2015-10-14', u'CrusaderKings', 4, 6, 0.4, 11, 6, 5, 15826, 7926, 7900, 0.0008975765433330009, 0.0017935432443204463, 9, 34445156, 396515], ['2015-10-14', u'smashbros', 1, 16, 0.058823529411764705, 11, 6, 5, 32733, 16401, 16332, 0.0004388103364212579, 0.0008772357327355134, 9, 34445156, 396515], ['2015-10-14', u'progressive', 2, 1, 0.6666666666666666, 11, 6, 5, 12731, 6308, 6423, 0.0009615384615384616, 0.001921229586935639, 8, 34445156, 396515], ['2015-10-14', u'progun', 2, 4, 0.3333333333333333, 11, 6, 5, 11328, 5636, 5692, 0.001101624896722666, 0.0022008253094910595, 8, 34445156, 396515], ['2015-10-14', u'guns', 1, 3, 0.25, 11, 6, 5, 30478, 15238, 15240, 0.0004197271773347324, 0.0008391021606880638, 8, 34445156, 396515], ['2015-10-14', u'EngineeringStudents', 2, 8, 0.2, 11, 6, 5, 16528, 8300, 8228, 0.0007615421227986673, 0.0015219252354228099, 8, 34445156, 396515], ['2015-10-14', u'RealLifeFootball', 1, 2, 0.3333333333333333, 11, 6, 5, 150, 80, 70, 0.0, 0.0, 0, 34445156, 396515], ['2015-10-14', u'Republican', 6, 4, 0.6, 11, 6, 5, 9899, 4947, 4952, 0.001243587750660656, 0.0024840863219996894, 8, 34445156, 396515], ['2015-10-14', u'reactiongifs', 1, 6, 0.14285714285714285, 11, 6, 5, 37026, 18488, 18538, 0.00033107101473266014, 0.0006619228859837829, 8, 34445156, 396515], ['2015-10-14', u'ProtectAndServe', 1, 5, 0.16666666666666666, 11, 6, 5, 15538, 7759, 7779, 0.0008207653637016518, 0.0016401845207585854, 8, 34445156, 396515], ['2015-10-14', u'Battlecars', 1, 2, 0.3333333333333333, 11, 6, 5, 1030, 503, 527, 0.0037313432835820895, 0.007434944237918215, 3, 34445156, 396515], ['2015-10-14', u'Gunners', 1, 4, 0.2, 11, 6, 5, 20257, 10178, 10079, 0.0007197696737044146, 0.0014385039558858787, 9, 34445156, 396515], ['2015-10-14', u'unexpectedjihad', 3, 1, 0.75, 11, 6, 5, 6889, 3394, 3495, 0.0014699706005879883, 0.002935625917383099, 7, 34445156, 396515], ['2015-10-14', u'IASIP', 1, 3, 0.25, 11, 6, 5, 15963, 7977, 7986, 0.0007755695588948134, 0.0015499370338080015, 8, 34445156, 396515], ['2015-10-14', u'southpark', 1, 7, 0.125, 11, 6, 5, 17601, 8777, 8824, 0.0006948666724572223, 0.0013887683360819373, 8, 34445156, 396515], ['2015-10-14', u'funny', 27, 85, 0.24107142857142858, 11, 6, 5, 162736, 81314, 81422, 8.505731918231564e-05, 0.00017010017010017008, 9, 34445156, 396515], ['2015-10-14', u'neurophilosophy', 1, 2, 0.3333333333333333, 11, 6, 5, 2249, 1138, 1111, 0.004366812227074236, 0.008695652173913044, 7, 34445156, 396515], ['2015-10-14', u'exmuslim', 5, 3, 0.625, 11, 6, 5, 10887, 5449, 5438, 0.0011574074074074073, 0.002312138728323699, 8, 34445156, 396515], ['2015-10-14', u'hiphopheads', 3, 30, 0.09090909090909091, 11, 6, 5, 39858, 20055, 19803, 0.0003579525116334566, 0.000715648854961832, 9, 34445156, 396515], ['2015-10-14', u'australia', 26, 14, 0.65, 11, 6, 5, 29720, 15036, 14684, 0.0004317556263155054, 0.0008631385876894858, 8, 34445156, 396515], ['2015-10-14', u'fitnesscirclejerk', 1, 1, 0.5, 11, 6, 5, 9374, 4727, 4647, 0.00121675647488267, 0.0024305555555555556, 7, 34445156, 396515], ['2015-10-14', u'4chan', 36, 32, 0.5294117647058824, 11, 6, 5, 40927, 20531, 20396, 0.0003355579583162447, 0.0006708907938874395, 9, 34445156, 396515], ['2015-10-14', u'unitedkingdom', 5, 13, 0.2777777777777778, 11, 6, 5, 30150, 15141, 15009, 0.0004750844594594595, 0.0009497177227879493, 9, 34445156, 396515], ['2015-10-14', u'wildhockey', 1, 1, 0.5, 11, 6, 5, 6608, 3287, 3321, 0.0013986013986013986, 0.002793296089385475, 6, 34445156, 396515], ['2015-10-14', u'BlackMetal', 1, 1, 0.5, 11, 6, 5, 7395, 3693, 3702, 0.0016427104722792608, 0.0032800328003280035, 8, 34445156, 396515], ['2015-10-14', u'paradoxplaza', 1, 4, 0.2, 11, 6, 5, 15384, 7720, 7664, 0.0008144980655670943, 0.0016276703967446592, 8, 34445156, 396515], ['2015-10-14', u'TrollXChromosomes', 1, 5, 0.16666666666666666, 11, 6, 5, 29697, 14899, 14798, 0.0004886524052557281, 0.0009768274814131437, 9, 34445156, 396515], ['2015-10-14', u'SquaredCircle', 7, 83, 0.07777777777777778, 11, 6, 5, 40509, 20298, 20211, 0.00036631527534698196, 0.0007323622752054683, 9, 34445156, 396515], ['2015-10-14', u'blunderyears', 2, 1, 0.6666666666666666, 11, 6, 5, 13551, 6729, 6822, 0.0009038526720144617, 0.001806072920194153, 8, 34445156, 396515], ['2015-10-14', u'rage', 7, 7, 0.5, 11, 6, 5, 23790, 11840, 11950, 0.0005195817367019549, 0.0010386238234339502, 8, 34445156, 396515], ['2015-10-14', u'createthisworld', 2, 3, 0.4, 11, 6, 5, 473, 238, 235, 0.009900990099009901, 0.0196078431372549, 3, 34445156, 396515], ['2015-10-14', u'RoastMe', 2, 8, 0.2, 11, 6, 5, 15824, 8181, 7643, 0.0008744656043528955, 0.0017474031647412873, 9, 34445156, 396515]]
for row in addendum:
  dataset.append(row)

import csv
with open('neural_net_votes_altright_intensities_network_structure.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(dataset)