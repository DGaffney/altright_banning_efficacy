from sklearn.neural_network import MLPClassifier
from sklearn.svm import NuSVC
import re
import json
import string
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import os
import csv
import pickle
import argparse
import itertools
from sklearn.linear_model import Perceptron
from sklearn import linear_model
import random
from sklearn.neighbors import KNeighborsClassifier
import itertools
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import ensemble
from sklearn.svm import SVC
from sklearn import svm
from sklearn import linear_model
from sklearn import preprocessing
from sklearn import gaussian_process
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn import tree
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np
import csv
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import SGDClassifier
from os import listdir
from os.path import isfile, join
import numpy as np
models = [
Perceptron(fit_intercept=False, n_iter=10, shuffle=False),
Perceptron(fit_intercept=False, n_iter=3, shuffle=False),
Perceptron(fit_intercept=False, n_iter=5, shuffle=False),
Perceptron(fit_intercept=True, n_iter=10, shuffle=False),
Perceptron(fit_intercept=True, n_iter=3, shuffle=False),
Perceptron(fit_intercept=True, n_iter=5, shuffle=False),
linear_model.Ridge(alpha = .5),
svm.LinearSVC(),
svm.SVR(),
SGDClassifier(loss="hinge", penalty="l2"),
SGDClassifier(loss="log"),
KNeighborsClassifier(n_neighbors=2),
KNeighborsClassifier(n_neighbors=6),
KNeighborsClassifier(n_neighbors=10),
NearestCentroid(), 
RandomForestClassifier(n_estimators=2), 
RandomForestClassifier(n_estimators=10), 
RandomForestClassifier(n_estimators=18), 
RandomForestClassifier(criterion="entropy", n_estimators=2), 
RandomForestClassifier(criterion="entropy", n_estimators=10), 
RandomForestClassifier(criterion="entropy", n_estimators=18), 
AdaBoostClassifier(n_estimators=50), 
AdaBoostClassifier(n_estimators=100), 
AdaBoostClassifier(learning_rate= 0.5, n_estimators=50), 
AdaBoostClassifier(learning_rate= 0.5, n_estimators=100), 
LogisticRegression(random_state=1), 
RandomForestClassifier(random_state=1), 
GaussianNB(),
linear_model.LinearRegression(),
linear_model.Lasso(alpha = 0.1),
linear_model.Lasso(alpha = 0.5),
tree.DecisionTreeClassifier(),
tree.DecisionTreeRegressor(),
linear_model.ElasticNet(alpha=0.1, l1_ratio=0.7),
linear_model.ElasticNet(alpha=0.5, l1_ratio=0.7),
linear_model.ElasticNet(alpha=0.1, l1_ratio=0.2),
linear_model.ElasticNet(alpha=0.5, l1_ratio=0.2),
linear_model.RidgeCV(alphas=[0.1, 1.0, 10.0]),
linear_model.LassoLars(alpha=0.1),
linear_model.LassoLars(alpha=0.5)]
models = [
svm.SVC(kernel='linear'),
svm.SVC(kernel='rbf'),
NuSVC()
]
models = [
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(15, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(20, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(25, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(30, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 4), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(15, 6), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(20, 8), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(25, 10), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(30, 12), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 2, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(15, 2, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(20, 2, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(25, 2, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(30, 2, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 4, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(15, 6, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(20, 8, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(25, 10, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(30, 12, 2), random_state=1),
models =[
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 5, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 10, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 15, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 20, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 25, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 30, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 5, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 10, 4), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 15, 6), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 20, 8), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 25, 10), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 30, 12), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 5,  20, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 10, 20, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 15, 20, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 20, 20, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 25, 20, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 30, 20, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 5,  20, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 10, 4, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 15, 6, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 20, 8, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 25, 10, 2), random_state=1),
  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 20, 30, 12, 2), random_state=1),
]
with open("/media/dgaff/backup/Code/altright_banning_efficacy/baumgartner_data_test/machine_learning_resources/inner_researcher_votes.csv", "wb") as csv_file:
  writer = csv.writer(csv_file, delimiter=',')
  for k in devin_labels.keys():
    writer.writerow([k, devin_labels[k]])



month_sets = {"2014-04.csv":["cgh334o","ch0cvye","cgzyo57","cgwc1wr","ch08qfd","cguivwl","ch2df40","ch07lrl","ch4a1aa","cgu8ol7","ch2r0xi","cghieid","cghcx2a"],"2016-12.csv":["day46xj","dbi2bic","daqtnf6","dbmace7","db4lccu","danvt6e","db30kpc","dbhdo4k","dbr651i","db531ga","dba1ewu","datab3t","dbc074s","dborm38","dauq28h","dbttu9k","das8d1z","dbrpht5","dayu9ol","db3ixxb","dbrhyey","dbit07g","dboh97m","db0r0r0","dbr5ps5","dbs4dqw","dbrkwlj","dbtvwc3","db7viqr","dbmixgt","db1p1qz","dbcq3i2","dbacd7s","dbijcvm","dbrk6jz","db79ajx","daq4djh","db79kyn","dbkq28g","dbra9k1","db1ibn2","daz76ht","dbs4mhf","db3o1ta","daoukkm","dbuiar5","dbkljpd","dbfcia4","dbq5d1w","dbftoa6","db1rfwo","db7s1br","db8wgog","daufh1i","daq8vnj","dbjfyw0","day2tyx","daus8x3","dbraruk","dbp12w9","db6g3iw","dbhd5kb","dbarinq","dbnl2xf","daw288b","danehpy","dbt34d3","davlm7u","dboa1yg","daodsd6","db8924x","dbhghzr","dbapk3y","db0luwu","dbswowl","dbcwotm","dbjrkkq","dbo3dqh","dapgaq2","darz37v","dbe2ky9","dbqbr1h","dbq7aoi","dax157i","dbnfyal","dbjwn9w","daom299","datra8l","daz0nwm","dbbj2lm","db8f7yt","dawe9nf","dbjogmq","daxrvja","daxplkd","dbhecvq","dbrj7or","db8cyih","dbrwb46","db8meox","dbae7c1","dbujeny","dbkaaw0","dbdavb0","dbqjry4","dbbuo97","dbbuyhn","dblao1f","dapi8ll","dbj3d1w","daowevh","dbav7f2","db3kgll","dbgovn8","db37cyd","dbcrjj4","dbh7va2","daw0o3c","db4abm7","darlkk8","dbcdsex","db5dgt4","dbgbuqr","dbsh2xd","dax5wd6","db6ctbg","dbm3v7l","db3zw1q","daz4bjz","daz443r","dbdb1h9","daxhbv4","db498px","dbd3pcw","dbhivwj","dbs5ywn","db74q6o","dap3ifd","db49uz0","dbncmng","db975iz","dbbvck1","dbngm7i","dapcc1a","dbrv8as","db4u673","db65k8v","dawjxdd","daw6zxu","db4hxsc","dbtuj6i","dbnpynj","db1ifz3","dav94ck","dapj6zu","daur87k","dayrlvd","dbrr5wy","dapti0k","db4g53u","db2qcs8","dap4spm","dapp29c","dbttqzg","dbssqm2","db3f7xp","dbp78wv","dbsfwre","daxqtxq","dar8okq","db13vpg","dblkcc2","dbsk2nr","db4ml9f","dbtz50t","dapyosj","db9draj","daof93f","db8kgqa","dbt45ls","db76g3r","darwoyu","dbbabkp","dbmjpj8","db6tsoe","db9hhtv","day504w","dbujgez","db5z9ok","dbjrymr","db8he96","db8bak7","db3m48d","dbaoqps","datif1w","dbufc73","dbt82ga","dao1tfw","dbnc7fd","dbax98g","daroj7u","dbpy1q9","dbnjgfo","datq2m2","dbbx5op","daxq97x","dazf7cp","dbis9hx","dbavm9n","dbrbx23","dbbgg63","datasbq","dbhib7v","dayxdf1","dbjcfu3","dbsbh7j","db88s0j","db6eqwd","db24vsy","dav3hjk","dbh32mv","db21nnf","db1k7oa","db9puan","dazq599","db36mac","dbilnq4","db71uf1","db6z8pw","dbpptne","db2ysho","db64bpc","db7s68r","dbbp9cs","dbn7p71","db92mtp","dan45xy","dbt4r5e","db082az","dazsfwz","dbspl59","dbsxe02","dbmql6f","dbs0o5a","dbckjot","dbdtuxi","dbpjbws","db37oon","dbt3zzj","dbrmm4g","daotp0c","dbm8v29","danvapf","dbmu6tn","dbobnk6","dbsww0w","db79th4","dann441","dbiu8od","dbpw6zh","db98b18","dbgxcno","dbkvwyo","daydnin","dbiyy90","dau66qa","daynzjh","dbpfzlw","dayqet0","dblivit","dbqa8zs","dbbg82u","db3zxyf","dbgm18s","dbt296b","damvj9e","dbidxoe","dbp21hz","dbibqon","dbhnyfn","das986s","dayvnp9","db7sp72","db4gc2c","dbjfuuj","db4g66i","dbeqvnx","dbdpjpn","db2t00s","dbspbh4","db7neo5","dau59lr","dbhrc0a","daul5h9","db4mk3h","dbamyd8","dazmnj6","dbs9gn8","db6hg2l","dbkfhsw","dbgl5n1","db0nklg","darqilj","db11vrv","daqr1cj","db9nhm9","daskf0d","dbjw2l3","dau7psi","dbdf5xi","db04qgu","davbb89","dbumgs4","dbdjgze","dbnzv5f","dbi52ub","dbjfpwu","dawyavg","db29111","dandsbk","db924ul","dasqp9c","dbjtlid","db7jgpu","davzhdk","dbdgvun","db3l3g6","dbrjvv4","dbl2wvi","daty004","db65n80","dbqnrkz","dbbzjgl","dat6abl","dbh8473","dang88h","dbhkvpo","dbrb8db","dbc6hzo","db998c3","dbodiir","db0exic","db525mm","dbkkevk","dbeovzx","db728x7","dbjhbor","db794it","dapci8o","dbsk9b2","dangn7d","datovh7","dbq138x","dbeqzov","dbt5vro","dan9nhl","dblhp2s","dbehj3e","dbli7jq","db7u6db","db1dt1g","dbl3oiv","daz8gtx","db2pe3f","db2qa0h","dbbcrrn","dan2piw","dbgvphk","dbsarpq","db39fjs","dbqdqvb","db7vuqj","dblrfzh","dbp5ti1","dbbmohd","dbsgad5","dbt7nt7","dbeeml4","db9ngop","db474ji","dbq9298","db167x3","dayfbps","dbntrby","dbt6qtd","dbqtrom","dapyu3x","dbckuo5","db427j7","dbtysbb","dbivmqs","dbsi5mj","dbtv71s","db00hmq","dbb3ml3","db0ead6","dbjvl6t","dbsmhfh","db8qdxs","dbsa587","dbpmf86","dbndmiu","dawhns3","davn0pj","dbkep7t","dayyeqr","dbkoy1k","dbsxwwe","dbbeby1","dbtn0yp","dbscwcx","dauhtzs","dasppxd","dbh1oi4","dbl4zq8","dbrzmkj","dbegfgf","dbm9r23","dbermd8","db3yk7f","db1kfk0","db7tybm","dbnr3bh","dav329t"],"2016-07.csv":["d5d5vjc","d59055f","d5xpcen","d56ijo7","d5vdulx","d59728w","d5rbv4x","d5sh6pm","d4ysbh9","d5tk76f","d5oexaw","d5przyg","d5voczl","d5po3t4","d5glltx","d5sihtg","d5ylvdc","d51x4zi","d59skhn","d5sapxz","d5h4m81","d50h29j","d530vau","d5c46s7","d5rdrvh","d5wyb9e","d4vog6p","d5uw33s","d5or0e9","d5rmc68","d5r5qd4","d58rn14","d5w5xnh","d5yf47k","d53a572","d5ga2lh","d5ubtyn","d5tl3lt","d5ch7ut","d55z2of","d4wc2s0","d5a1dzq","d5fgnrm","d4wu38g","d5sf775","d5rqhod","d5w3zdv","d5lrmsm","d59b6py","d5seowk","d5cf0xg","d5u829s","d5p2zk7","d5i0c9k","d57aq1j","d5uojjn","d4wd196","d4z6sv0","d4y756w","d5bpa2y","d4z7rre","d59d0s6","d553guw","d5dwwon","d5mdx2h","d51pfe2","d5hr4rt","d5i6824","d5a2iov","d50u6db","d5wjg78","d58m9om","d53lhhx","d5cmh3s","d5cf8ik","d5xpc03","d55omio","d5m1htf","d5bdadj","d5v4zfb","d560u49","d4xxmsy","d4zobz5","d56zq23","d5ekos9","d5w0l9m","d57jmxe","d5tr4zi","d52f5xw","d59gm04","d5nz4nv","d5xmgdp","d5igoiu","d56mnsc","d5fpost","d5g9xic","d5ndr3o","d5ply1m","d5u4he5","d5kwey3"],"2016-03.csv":["d16zq2q","d0q897p","d0sagr3","d1gkzuq","d15sjyn","d0x2qmm","d0twh9o","d14urf9","d1dmpab","d0y8ssw","d16jfmg","d12oul0","d181753","d1iq32v","d0ojklt","d0o3el5","d19w82e","d0n29ow","d0uo3m6","d0outxw","d1e0e3j","d0vzk42","d1hejck","d1amme3","d18yhii","d0uyhyg","d15fs20","d13lz34","d1hp0a1","d1030m4","d1kffl4","d0n98q4","d0ulkeh","d112jc5","d0p09he","d10fui1","d133z9z","d0zw0ez","d0q6gva","d1049eg","d0ncrx8","d1j73na","d0yvhfe"],"2016-09.csv":["d7gytws","d79l9nk","d822v73","d817x3d","d7vcot5","d7gawe7","d7v6ejx","d79s9nv","d7wwc8x","d80lqlp","d7ixbm9","d7m2mpu","d7opm6r","d7gbbgy","d7iqpiw","d7t2kp8","d80mgg7","d7620qc","d7w6o84","d75y721","d7pv92d","d7xr20a","d84ff1i","d7akr2f","d77bnau","d84aaqo","d7b0czv","d7fdzlg","d7jmj1l","d7d9rkf","d7xos4x","d7nm2ij","d75awr9","d7n1nmz","d7ltcak","d7x2zmc","d80ulpa","d79k51g","d88x2c6","d7u0vlm","d7o45by","d87agwi","d7lcja8","d7im7so","d75f2co","d7y7p91","d803vx6","d7610ec","d7q2pmw","d7n8pwo","d7fhu3q","d7zhus3","d78lfs0","d874fwh","d79w40t","d7yekv4","d7m083s","d79qhd1","d7knoi1","d84qe3u","d79xdmt","d80bl3p","d7sop1f","d81yhfy","d7564oy","d87uvkh","d87ijcr","d787yho","d75u62k","d7j9wqx","d78i92n","d7ds95v","d87egcl","d7b2xnf","d7bf0s8","d7tyf4y","d7gqijp","d82firz","d7cit76","d78vel3","d755lyk","d76vzmz","d74t8dp","d7vde91","d7mrcyn","d7fa8x1","d7jc7hb","d7y5z1p","d8143rc","d81tlpg","d80rzda","d7obbbk","d7ysqtt","d74xvfw","d7gc3x2","d866cjg","d7evwrc","d83cm8c","d7kvneg","d7ox3sq","d7h71dd","d7vy1bi","d7jyfny","d7gp9u1","d82ou2b","d772ogx","d7p9kb6","d86dlf9","d7i7fce","d7assiw","d7zw4i9","d80ywf8","d7fehfe","d7g67m1","d75vses","d7mto9x","d7vfdjq","d7wq95u","d87ehrj","d79ccjr","d7umvx9","d832ff4","d80513r","d7ou4nc","d7w9t00","d824rxb","d76503h","d79qjel","d7wib92","d7qlrr9","d7oj4x6","d7u250r","d7xa2h2","d7t6cmd","d7p1ip1","d7fitd9","d79z0ca","d7bosli","d7dsste","d78dk8y","d843jn7","d7nxhpi","d7xe8zn","d7cht0y","d755jkg","d7a7heu","d7ni5nv","d7unk57","d75hj9f","d7nalnf","d7d0w88","d765wli","d82sbof","d79n5e4","d7n8siz","d768x06","d7z9zw1","d7y1ul6","d76ljuu","d82h782","d7gpt3f","d7qhcpf","d800fox","d7drvtf","d85shst","d7gphzj","d7wx2kl","d7to07k","d7uwk72","d75hz2k","d7729cn","d86or17","d7bgbxg","d75y6io","d7epp0g","d7lk2d8","d7ljyjc"],"2015-10.csv":["cwa8zaz","cw8w5b5","cw6q1bd","cw5bep8","cvqzo4w","cvq4xd3","cvs6sot","cw7sfi3","cvltjdv","cw76ynm","cw1aw2s","cw7ygvi","cwh7q0l","cwiwzal","cvn6mlu","cvwpwwi","cvkaoma","cwhr9nr","cvjz632","cwdvvho","cw3nsiz","cw6wetv","cvxrd47","cvz2q0r","cw2mbwf","cwggxwc","cvsif86","cw22ewh","cwencbn","cwfy9ve","cvrjcsu","cw11bz3"],"2017-02.csv":["deah8bg","ddnjgwb","ddde43x","ddo5gyb","ddn9n24","ddofz69","ddb3sqd","ddm5bqy","ddws35p","debppsm","de6sw46","ddarq5s","ddmwhhv","dd7g9by","ddkb5e9","de8k2hn","dd8on16","dd6j2pf","ddlqb8r","deaghhu","de9mvaq","de5faqo","de7nbqr","de2v8bu","ddkj3ea","ddopx4e","dd63num","de4y8pj","ddz9zgb","de10fsg","ddpksyt","de6kigu","ddk4428","ddhmi5p","ddubza2","ddiakq8","dd74x94","ddr0n6g","ddb1dvp","ddyae1n","ddi04rl","ddu5o9h","ddop1yl","ddvm7yt","ddbfjsn","ddfs2z0","de62ikb","dd7s1q3","ddbajht","dec2zqf","ddcgd19","ddeyych","ddx2a91","ddr7mpu","deag7mg","de2wdej","ddnh1qq","de56bg4"],"2015-02.csv":["cob302e","cotziou","comcvvz","coyj7qc","cofd36g","coir6pt","colwl6e","coqq634","cofwnim","coohh4i","copsob1","cof5uy9","coqu5fh","cowcuyw","coemm89","co8sr4s","coe9udw","cocptcm","cowrvr2","colymc2","cour2tc","conqjr5","coalytp","co9p751","cor7dor","coc6q9j","covn078"],"2016-08.csv":["d69dfv6","d6zd13t","d6q61p5","d6io1lz","d6pjdln","d6usbgd","d72lagj","d6kpwkp","d72w9s3","d6jen4a","d6mpieb","d6mfb8f","d71ynux","d69hcog","d6m1g96","d6z1nad","d74iyzq","d6hhrlq","d6yqb1h","d6tcfpa","d7413r9","d62469c","d6x6lab","d63zlrb","d6q0r0d","d729eom","d6r8j8e","d61aeqi","d6yv232","d6c8qxz","d6gmipj","d6bovjt","d6cwkrl","d67hll3","d70yh6j","d72t9v2","d631tbf","d7050iq","d726vxr","d60sttg","d6zb23h","d6zrxbi","d7134ea","d61zl6y","d72e3gw","d6pjjxr","d6jwskv","d741c76","d6u84x0","d6nwmv3","d6m3yrb","d7374an","d6n85tk","d6wkfiu","d62x5wb","d67l5f8","d6zpe9b","d6uxox4","d6qi9ve","d6dbh5a","d6qu30a","d72ichd","d6x5ln8","d68eo9d","d6z017u","d6z3b2a","d71mlgp","d6be6sp","d65lmgl","d5zu81k","d6fv9j2","d6b2ng0","d62defv","d6zlywb","d728gkr","d6kw60v","d6pusf8","d6r02jw","d6etsex","d6x3g5w","d67pxid","d72q7li","d6q38ww","d6tkmxc","d6bnbbv","d6icjje","d6v4lzf","d73w5ze","d71j1fc","d70yv4j","d6tbut2","d6gz67e","d6cw6co","d6wyyyb","d6zyqc9","d733hd1","d6u2129","d6014y0","d711wf6","d6xheqv","d73mnzv","d5zli62","d6wprch","d6gbu5j","d6b8wys","d642afz","d64w0vz","d61ntup","d6k4jfx","d6kiqyl","d6jg4ea","d6r7xwl","d70yw33","d71ki67","d6bekh8","d6er09d","d6yelng","d64ps38","d6hhu0x","d61fcoo"],"2017-01.csv":["dc9beww","dc20hu4","dbzsjp6","dc4whs0","dc8kd43","dbz216w","dcyvy8m","dbz686c","dc0hz0g","dc3m5v7","dc7rnd7","dc2lfi3","dc2msn2","dcawx42","dc1ndo3","dc72jo6","dcj0r2f","dc7z74b","dc4y3z5","dc9gziy","dc5wrzj","dc1yqoq","dc0xzgp","dbxszw4","dcbjrez","dbzpa1w","dc34v3j","dc6co2f","dc6thqz","dc3c8nu","dbut5o4","dc518yt","dc9sfo3","dc9gs3u","dc9nndo","dc9fku2","dc4v7a4","dbw0pgo","dc9l5ma","dc50ix1","dc3zht1","dce8khu","dcmub8d","dc4lofy","dcatchu","dbvibnx","dc08hz8","dc09so7","dbxksvq","dc69z01","dcba8en","dbzivy5","dc23f52","dbyf7kp","dc6p7ik","dc4vw74","dbx8exg","dd55uxr","dbyvx15","dc0fz6a","dcqu54o","dc6k6dp","dcn0v3u","dcdi6ld","dcbgzws","dbupo59","dcbxju1","dc7nh6o","dd131vs","dc9ncgv","dc93uku","dcmume8","dc1prov","dbwd70x","dc260tb","dc0i552","dcas09x","dc9kwb8","dc01tgu","dc6cahf","dc2fcmv","dc9112r","dcm4kqv","dbutszo","dbyk6ae","dbwbeqz","dbyp0ps","dc3srg2","dc3ktmb","dbw9d1u","dc0hxmq","dc24kdd","dbwv9fa","dbunc1o","dcflzg5","dc7lueu","dc4tzvc","dc4mh2x","dc7388s","dc51pg6","dcywrjt","dc57p6u","dbwzj0m","dc9d1h8","dbymxls","dc6dfi4","dbuv6ox","dc1hysi","dc0zogz","dcijcag","dc0bald","dc6ra4a","dbwnhyb","dc6nlyv","dc8size","dd536kt","dc49wn1","dc6w6zv","dcfpjqa","dck8at2","dd1ja9g","dcwxnkz","dc5vfw1","dbw755s","dc7vubv","dcshyl4","dd3gl9z","dc0mf8x","dcavf6t","dcbhid3","dc853yd","dcb9dge","dbzvyu5","dbxsc8l","dc5l98d","dcztnb1","dc82q2h","dbvij25","dc5jsu8","dbwanv7","dc2564o","dbzbrmn","dcdw6y0","dc5qq9l","dbyyxfd","dc5z8ox","dc90gy9","dbxp1il","dc4w9rx","dbwx00l","dc9x13q","dc05ixv","dc2rtnm","dbzleri","dc2umus","dbvyq3m","dc7bqme","dco93qi","dc8k1w2","dc8rsev","dcb2lfk","dc4pevn","dc8hnny","dc8d718","dbxeue8","dclcmls","dc7ru9y","dcx4k4f","dchgv19","dc57j9c","dbv18pe","dbyxbe4","dcfda3c","dbw6cpe","dc9m82p","dbwhx4l","dbwjktj","dcqkgb1","dcau2vm","dcaqwv0","dc8h1f7","dc7x8df","dd5yf1t","dc5wp9u","dc93agw","dc4qzfn","dc1ioa9","dc33ye9","dbyir29","dc5wioa","dc9ltar","dbxm0t9","dbw07wc","dbyq8w5","dcsato7","dbzpmg0","dc6xbmj","dc4r9oh","dc7u06e","dbzb26j","dcbk82f","dbw08r0","dbz1cx6","dbyruy8","dc41330","dc7raer","dc5z2i1","dc9frxz","dcb8rer","dd5f0gm","dd26uk5","dbxnpks","dbw9yz2","dc2odev","dc9ting","dc31h53","dc19deg","dbuuoku","dcfny6z","dca9upk","dc4yhrb","dbwor39","dbv3x19","dc25kt3","dca8lq2","dc2atil","dc50r9d","dc1x6id","dc934cg","dc7cokj","dc0fifl","dc5czkj","dc696ev","dc8izrg","dc4388e","dby1l58","dc2l59n","dc1pa7e","dcrg525","dbzckt7","dc4bm6s","dcp8qy7","dc5bhls","dcb8nlr","dcbhifs","dbxr3e1","dc4ylof","dbxlju0","dc2zh7z","dbwd430","dco01qi","dc1casl","dc59erk","dbvt2gl","dc21suu","dc5s6tk","dc2h5au","dc91mlu","dc60xo9","dbzu4ms","dc3qt1e","dbvp4vn","dcy26yh","dbwuyvw","dbv8tqe","dc3m84p","dc1b4bm","dbybbys","dcstnao","dc4x8no","dcjzura","dc8fmlc","dc0lbbd","dc1ogny","dca5mf2","dc5ypmt","dby2v75","dcm1d5q","dc9b8b0","dd5wopq","dd5ld2p","dca1epy","dd2y506","dbvgfxs","dbwoql5","dc3t7ml","dc6lem1","dc5rbkw"],"2016-04.csv":["d2kdlmh","d2auwv4","d1qemi0","d1uq2wk","d27arze","d2b8npy","d1xec9w","d28wuxu","d2502df","d21oxkp","d1ya83b","d1zfnud","d1ws5j5","d29ovu6","d1p1c0q","d1sncdc","d1xivxx","d25758j","d2kgzdr","d22xamm","d230lfv","d2478k3","d1llvq2","d2a8adw","d2muda2","d2d9n7u","d2652vc","d1oih8u","d1yy62s","d1sn1e5","d1pug1e","d2eu78e","d1sc2kv","d1tjgs2","d2nqudt","d1okkeb","d1y8wnr","d2lua3i","d2jdaa1","d2dwnl2","d2enuca","d2ei5io","d1u7rzu","d1smgj3","d2dg521","d2ifeqc","d1mac8o","d21tzuc","d29eh4o","d2ee7ov","d2mmst2","d2gqzbt"],"2017-04.csv":["dfy24af","dg9i8yf","dg29epi","dfonei4","dglijq0","dgd0eh3","dgon9wg","dfzi7a0","dgxlrf2","dgdj96b","dg7zez0","dgxczci","dgfydpx","dgccbzx","dftex6i","dfvr2lf","dglx2zn","dfvqtdn","dgf006m","dg10aq5","dfpe4v0","dfu3olz","dgoqbro","dg5sjy4","dfxcv78","dgumghx","dglt3ke","dgy0gil","dgylubv","dg86q5k","dfzsjz7","dg37l54","dg55ora","dfwx6cn","dgygyel","dftx627","dg9kned","dfzc4bo","dfzb2al","dg9l9b8","dgoetee","dgrd4aq","dg64gy4","dfpapf6","dfunmdm","dg9sjrj","dgvue2x"],"2016-11.csv":["d9lx16l","d9xfa7u","d9h9g13","dal8yxs","daigz8f","d9rtuyu","da4uwoj","d9u4299","d9xhldx","da16eve","dakir6n","da9fsy3","da941ff","daad8zj","d9lxspi","da2x216","da1v2c9","dallpu6","dak67i8","dak91nq","dah1vw8","da3fmc7","dahetqc","d9hv7h5","dal58ge","da4f0vh","daarubd","d9sy8xn","da5fgp1","d9wuq4c","daduft4","daftgyf","d9vtchw","da3sash","da2fgtt","dafk5ul","d9qbihm","dacd1w9","d9lkqjo","daeibqh","dalhilq","da9o9rh","daex4re","dadker6","daex8b5","dagqobl","daacj03","daklgep","daljh63","da2276f","da9f807","d9xuf6r","dain9z3","da31ztk","dalsxac","d9zy22o","dabthmv","da0hjcr","d9u9el7","da3fyl9","dab26l0","daldhbp","d9ogjoz","d9nnxfx","d9xu3rq","da0378w","dadt619","daldeaj","d9o0bl3","d9h67ua","d9ulciy","d9w3k6k","d9wa2f9","daia9i9","da4ikiy","dahfbiz","da7dqla","da0v8qz","da8jfwc","d9o5nr1","da6l6ki","da42rni","dal3vo7","d9sciy5","dabrz3g","da4npev","daj5kwu","da57tic","dajwizz","da8vqby","d9yz2bn","da7w4q4","daimhbj","dakswc5","d9gdsbb","d9q44zj","daafowc","d9ifr6x","daaevdq","da7ua9s","da0tqv2","daal6x8","damnrw3","dabucc2","d9tt8lh","da81a76","da28w4r","dagsw4r","daeo9wr","da9epxl","d9iqw1c","daiss70","damgeru","da7rf7q","da3lp7r","d9wjenv","da6axhr","d9sh06f","da3f6ys","d9tzqmf","dalit1t","d9s9dwz","da5qpzj","dak79jb","d9x01g4","daeafcd","da74zyc","da49ykv","dajdsr8","da3jhc3","dacp6cu","d9o149e","d9liifq","d9vkldl","dajylyj","da8ubl7","dag9jez","da83ue0","d9ylefb","dahyqh9","d9wnzoh","da2c9qz","dakvkqe","da93ef4","dac9kv8","d9pq69w","d9z776o","da2ee6s","d9tr4xb","da84ynl","dalht16","d9mtcgi","dal6xdy","d9qd82s","d9ktr7o","d9wnwuj","d9kmxq1","d9jt2b0","dafb3c5","d9o1vv1","d9qbetw","d9vh0u9","d9hxht9","dac4y9e","da4gun4","dadtz6g","da6phr6","da7u0wj","d9hd6pr","d9rt98r","da0acjz","da6kgto","d9x0ato","daecga2","dalhu7e","dahw6hp","d9ix7qe","d9wfv9f","d9uuoko","d9jxqu0","da460c7","daclvvj","dahjftx","da3kd87","da023he","dakild5","d9vz7ay","d9oian4","dahuvey","d9vyodb","d9m1o62","d9ni1cj","d9gnnbv","dalm8d9","dakdrvx","d9te51p","da9e1fa","d9vqrb5","dahywo2","da8u5vi","daet1c2","d9u9fxs","dadsg8a","damfsix","dalnmbo","dagjx38","dabryuk","d9r35sh","dab9rih","da5ixv4","damis4w","d9tb1dn","da69vhw","dalbaff","d9zdnd6","damfej2","d9qprjf","da6fq9s","dakutz1","daavn5j","d9h24im","da962yf","da764yd","dad36g6","daewiy6","daj2epf","dagfe2g","d9rb9p3","da6lv9u","da9o3tn","dafb336","d9lg1p4","dakoxv1","d9wzc2e","dadzus2","da7b652","d9gaypx","dalqby9","da8ikh1","dak3mbk","d9yclbr","da8uwwy","d9kl5fn","da2nkfi","d9lppcp","da413nl","dad8nf8","d9ww8kv","da6hb1a"],"2015-12.csv":["cy9gp95","cyd7y5u","cxysydj","cyhjw6p","cy2zhhb","cybfu1y","cy3vlcc","cy1m2cl","cxys51m","cxwi9ir","cyhe1cm","cybnuqc","cxm9avk","cxqv4gu","cygkxdi","cydgi1q","cy47267","cxuatgx","cy5wrrn","cxn9y96","cy4n3w5","cxj2duu","cyakvl8","cxtfck2","cyezl6t","cy2xm1a","cxp8a4j","cy0i1a0","cxj0j3l","cy9hyzf","cy0bm1k","cxv5pnq","cxk2ce3","cy8ywa9"],"2017-03.csv":["df3zn35","df69snv","detcvbd","denapks","df7lads","demgbby","def7qy7","deri625","dfnn3w0","def3jmp","dfcgv41","dewkt23","df6mq9a","dfnby9p","dfbs10q","dfli13m","dehbubf","df8e1ls","df8i8y0","dfmvebf","dfcj3bv","dfo8bdh","dfcsns1","detnfxy","dfn8jqt","dewibiv","df1mpn9","deecw0d","deobl8k","dehpucu","degjha9","deus36g","dfkat1c","df32y02","dfmgxqf","dfbbwxv","dfhaens","desjsqk","dek199a","dfm0w5c","dejk3v4","df4cbum","dfa76g8","dfniyjp","dediibc","deell20","dffr57z","df0xko1","degyu50","detn8e9","deef6gm","df3uljd","decsvk4","detline","dfah3ta","dej6buq","dekepdc","deqx15g","dfg4o8d","df8ugjm","deh0e3m"],"2015-06.csv":["csez6fu","csbpskd","cslxu1f","cs6jy0c","crs7t1e","crt3f94","cskxjqp","csb2s0b","cs0qe2g","crsn7dt","csfmbaq","csilgc1","cs827pu","crvwodr","cs656el","csg4ycf","cslaup6","csm48uh","cshbdea","csgro7w","csd2v9k","cskyy5h","cs9o0v0"],"2016-10.csv":["d8nlebo","d9co1t9","d9ecjn9","d98c1bg","d8sp19m","d998am6","d96ykd3","d8cq7sm","d8h8i2l","d8pma2l","d98g5n5","d9eldrs","d8d2ygb","d8ncmli","d94gnya","d8kzdw7","d8936wp","d8gdz91","d8n8xwo","d92ikhz","d9087lu","d99vwia","d8lz05l","d94opoh","d8v3gcx","d91k6ui","d93zgs9","d931f7i","d8v570p","d8l2ccm","d91w073","d8ieeag","d9fbttf","d9g0368","d8fedul","d94oe33","d97gw62","d98te6s","d8oklkj","d966ue2","d8x4sw3","d8yh7fx","d9e03bc","d8wupjz","d9dx3sp","d91aw6f","d8uu6am","d9e9b5n","d9fqq2e","d8ztdsn","d8ezu2d","d8xc3ld","d8jx61m","d94tuzu","d9b0pw7","d8jrjzi","d99do3h","d9cdh0t","d99nf9m","d91zx7g","d8zzpby","d9a2kal","d8yn45w","d8d57ub","d8cklgx","d90jj2s","d8zpqj3","d981bc2","d8jsbps","d8rrgpl","d8dzue8","d94akr3","d91b13s","d8uz42o","d8sfbkd","d92ne4d","d8nzd6i","d94jfcr","d97zu97","d97fzz2","d95z9on","d8vgkib","d96ojh7","d8mzei3","d8umjpw","d8sgzla","d8ms89l","d8lkxl6","d8phhx9","d8pfm5l","d8nowwg","d8pxw8y","d8wswxl","d8bxhb2","d8dzu23","d8sq9x4","d8rgux2","d9cuffj","d92sxw6","d8os108","d8vi1ua","d95c1b7","d9a0f5m","d8vbxea","d8br98a","d9de1bi","d89dcwd","d94e239","d99p7ar","d90zfem","d8iofxq","d8jmhke","d8hm44h","d8z5mmy","d95khhj","d8bkpk5","d92rn7n","d98mll6","d8z18ie","d8g2lnn","d8q6kvf","d8w18o3","d8pcw4k","d8kofy7","d8mf89h","d94nzxn","d8jwrqp","d8wkzlb","d929mi3","d8pz485","d9eb4fe","d90wots","d8pcvzd","d8muyy1","d8jvuy8","d8990fb","d9a1tvg","d8hhiok","d9b2lqp","d8j0ugm","d8qz07h","d9enmya","d95iqwe","d8ex3xc","d9f3dsq","d90j6x4","d8uzuyb","d8gzxzd","d8mxfc5","d8kdod6","d9a64r8","d8ib111","d8gtml8","d95a9sg","d8jtyvm","d89w6si","d8zt6mq","d8prqze","d8tgzge","d98w0ht","d9f2u9o","d99wdcj","d94aint","d9c3ndc","d9bcdkm","d999657","d9ec1hj","d94ca6p","d8tksg4","d9ft7ew","d9crl5f","d9cgqme","d9chtf4","d8imqd4","d8lmpxf","d95bf8o"],"2014-03.csv":["cgc36y9","cfsvcyu","cg3t8ia","cg1kn9a","cg0zk7a","cg54sng","cg0sq1e","cfuj123","cg444j4","cg68p75","cg7f3pm","cg0haav"],"2015-05.csv":["croqrsl","cr2w1uh","crc35le","crapplc","cr1tl85","cqwbj8l","cqx9bmz","cr4gba7","cra6fuj","cr9m89b","crl3fc1","crh3jg0","cqvcmqn","cqvs5cn","crkzoox","crff6xm","cr2x9t7","crbkemq","crnyhq3","crhu77l","crkpd8r","cqw73f1","crmz9ez","crlkur6","cr70gtz","crlohz1","cqwtlwq","cra7lq2","cqut6xh","cr1zp7b"],"2011-05.csv":["c1svs3i","c1tjxku"],"2016-01.csv":["cyzgeza","cyqld6q","cz7xweb","cz4od10","cyldfj5","cyqxoch","czbwa5y","cyykflg","cyrzyle","czhiduc","cylkpkd","cz4fglw","cylfz28","cz2wj7r","cyms705","cz84bzm","cyp05f1","cyljpst","cyjszjs","czdxg1t","cz1rmor","czb0odi","czibjih","cysfpzs","czec8bn","czh6kky","cyi4m3c","cz3b28h","cyy3vqb","cz557u5","czemqp0","cz6dynb","cyik7na","cz5vm6f","cyvjvkg","cyl8udf","cz83e4n","cywowge","cyjbp19","cyld0ns","cyxrskn","cyziebd","cz6n5j1","cz6cftw"],"2014-12.csv":["cmtqg88","cmz0ea6","cn5x44x","cmv3cvo","cmwsqw4","cn37qxp","cmrtw1s","cmp28j9","cn09gza","cmlotwz","cmjjx15","cn5x1ja","cmwft94","cmm9owj","cn66g0h","cn58tqr","cmub2fp","cmpnbp7","cmi079p","cmtml6s","cn9wkys","cmyan45","cmt03xx","cn7rrlx","cmn06p7","cmlczmh","cmr3395","cmtfq8z"],"2016-05.csv":["d3h8a7w","d2pymj4","d32vzc5","d3qky5r","d2xh975","d3p6xjp","d3pamig","d3djkix","d2woy76","d33aq61","d3hk0jb","d2oyp0l","d3b40s3","d2qj7ou","d2uj83k","d3ar01m","d2qaqjn","d3jcb6f","d3f5ix8","d37rev7","d3qzyl3","d36wbsq","d32xuzm","d2zkw4f","d3fa73w","d31y7bu","d303mun","d2o3t8o","d2xygdz","d3qi4sj","d3avihd","d365jdt","d2zljil","d2v9owe","d2todgl","d2r5rt0","d2pfkqa","d3jp951","d36kgki","d3or4ni","d2t9x73","d2scvbe","d3eymo8"],"2013-11.csv":["cdc9vfj","cd5g68a","cdlrqru","cdi8t17","cdkrt3p","cd67eyc","cdjafw6","cdkcpih","cdavee8","cdedmvu","cdb5kuw","cdeuuw3","cd7vmrd","cdo6u3o","cde8t4z"],"2015-11.csv":["cwthn25","cx73vmh","cwua146","cwslxwy","cwxhan3","cx4jaeo","cxcyd01","cx1n4gq","cx4pjal","cx286es","cwlbsj2","cx1qrvv","cwse1to","cwybvcy","cwkonx1","cwyaja6","cwp3w17","cwzzv3t","cwv5df1","cx5p1vy","cxemggj","cx2sj13","cx9thkc","cwyzcdj","cxdjc4i","cwk2pka","cx5leuk","cxbuupy","cwxlyp5","cx8zun8","cwqqyb5","cwpzfb6","cx9x4uq","cx9r2id","cx5bwge","cxajifj","cxfw45c"],"2015-07.csv":["ctc0ivk","ct5zw6s","cta45vy","ctm7tt2","csv8wdn","ct0q6yl","ctf6vhi","ct8dx93","ctauu82","csru9ed","ctetcrz","ctdh0ga","csyuo07","ct3gyao","ctd2dlk","ctes9me","ctfgply","csxstgv","ct286o7","csriqoa","ctfmvf5","ctkw51s","csyuas6","csrglz3","ctlt6b5","ctfzu23","cti9xdz","ctkzqum","ctb78u8","csw7btq","ct95ijg"],"2014-01.csv":["cefheyb","ceh7b64","ces2b2i","ceutqhi","cez06zr","ceslf2q","cew9zbi","cew1h9r","ceiosq6","ceu3k03"],"2014-10.csv":["cl44uq6","clbye50","clgmy0s","clj2zck","clc46qx","cl1m2tp","cl6bwd0","cl37i9b","cli4e02","clnch8h","cln2u2o","cl7sb1x","ckzx2w8","cldam7o","clo5jbk","clhy330","cl4yvod","cllp7uu","cl3hj5j","cl1qts9","cl8b204"],"2013-06.csv":["caj7dcn","capkcvz","carxzwh","cago39g","caebapt","calac1m","cabn85s","cab60g8","canlgcn","caf5857","caoh9xo","cadtj9z","cafhcab"],"2014-05.csv":["ch9hyt8","cha7d9n","cht5jk3","chlwynh","chvrnm2","ch7mguc","chl94r1","cha4c7l","ch7e2gn","chib36d","chhath1","chfmky2","chntz9e","chtkq0x","chg0mg2","chq9pc5","chdklvj","chmfigm","chagubs"],"2016-02.csv":["czxnx12","d0frn9t","d02ssd1","czqbp9x","czmvcbm","czvbhen","d07yhtz","d0fodm4","d036h13","d03cje6","d01k4jw","czsteo6","czos8ox","d0ex82t","d016s47","czvb1m2","czj62ey","d0duimi","d0ekkqo","d06bxzx","d0gm1ya","d0enswv","d08e1ce","czuo7qs","czk1uso","d0bltlx","czq6z5z","d03s1z2","d09d182","d03nus1","d043ye4","d0dghds","czuph1s"],"2015-09.csv":["cuystwq","cvd9gz9","cvjqrqu","cvagiq9","cuukew2","cv8zgsn","cv90zfr","cusn2bx","cuup10n","cuzb7xr","cvh886j","cv7i0qe","cuyrt94","cvd1foq","cut2vab","cv06dph","cv0v4wa","cvd9qaw","cuykqos","cvgvyj4","cva2ap4","cvhnbal","cuycg72","cv343jj"],"2013-04.csv":["c9htq76","c9j9a8g","c9hg6mp","c9g06dc","c9nhad9","c966skw","c9p8mpb","c9gvir7","c9hs9ij"],"2013-02.csv":["c8b41kj","c8m92gj","c8cjc57","c8lo465"],"2013-03.csv":["c91r0yk","c8q7yib","c90luuu","c8t99j3","c93kioo","c8yt4x8","c8pys0j"],"2015-01.csv":["cnxkpz3","cnbxvlx","cnsgqe0","cnddz24","cnpelv0","co0e5e8","co0mqcp","cnmigso","cngg6ut","cnyf7ms","cngn7m1","co0pnb2","cnl3n24","cnmixnr","cnfgh2e","cnvtwax","cnuwxp6","cniukro","co013c1","cndhhun","cnzrx67","cns3gl0","cncfjzv","cnjtinx"],"2013-09.csv":["cbzxnuq","cca1cz8","cc2h158","cceqa85","cc5ohy2","cc6ykep","cc6q2n4","cc4ekor","ccgrkri","ccag27p","cc7tzvo","ccgrmci","ccf1gtv"],"2010-09.csv":["c10pled","c0yzqxf","c0z2vjr","c10oaix"],"2016-06.csv":["d4k69cq","d40xmu7","d4bh220","d4s48te","d3zsuqu","d4rbyx0","d4sfq5e","d4ivvx9","d4nctq0","d46s2tg","d4awp69","d4oozfh","d48uqam","d497wja","d4o0ubl","d41jwvm","d4b8k02","d4gvk0e","d4fed84","d4t5k6a","d4ndugj","d4qbz6s","d42ww5o","d4qy19g","d3u27de","d4ntze9","d3wltz8","d3vi1wb","d4gz63s","d4rr6dx","d44c86m","d4qj4q9","d4tfcn3","d3v18gj","d45qp7z","d4m2bwu","d4mmkr1","d4byor9","d3v2pmy","d4um530","d47j0ei","d4tcr03","d4mo9ox","d4jiefh","d4po3mh","d4uf0mb","d4uozf7","d4fcewd","d4rfxtw","d4h1wwj","d4jfez7","d4863bu","d3xsgok","d4nmxym","d4oa3xl","d42817f","d4mur4b","d3x8au4","d4tqaxi","d48zqpi"],"2013-12.csv":["ce0f0qg","ce5houh","ce8la0s","ce1g9kk","cdy8slc","ce0yu2l","ce6dl6p","cee19mb","cdsku13","cdxdu58"],"2014-07.csv":["cj1ee1x","cj4f2cr","cimftbe","cimbpoi","cis9qag","cj8cytc","cjben9v","cisw78j","cjbxpnu","cjbp6jd","cj6t3l5","cj0vnaz","cipfmid","ciw8ceg","cj8z8sz","cj9m7u5","cj4j48l","ciptz9z"],"2013-05.csv":["c9z75o7","ca9hnly","c9qjhr7","c9y8562","c9vsc5u","ca98qxq"],"2010-11.csv":["c14gusc","c169x9e","c164vbg"],"2012-01.csv":["c3l19wr","c3m6hfj"],"2009-10.csv":["c0f5t9x"],"2012-10.csv":["c6im53p","c6htgfu","c6jiu2w","c6rvxdf","c6mfkgz","c6nw2zo","c6k3yt9","c6ov9nv","c6rdnbw"],"2010-07.csv":["c0tw0r6"],"2015-03.csv":["cpemzbj","cp3bzhd","cptf6yx","cp2do7j","cpvevzj","cpooywf","cpfy4mu","cp2m79e","cp5vyzw","cpf29n5","cpcnp39","cpil7v8","cp1pg9t","cpf2il9","cp1fum3"],"2012-08.csv":["c5stahf","c5py5xm","c5rx15m","c5wyqyn","c5qspr2","c5xhpjh","c5u2wya","c5td8hw","c60ekxi"],"2009-02.csv":["c07r65g"],"2015-04.csv":["cqejj69","cqovwwn","cpyevey","cqjekza","cqqvdxf","cq5s6vi","cqi4mki","cqivfkr","cq85lr7","cq2w08m","cq18gaf","cqfpqni","cqamlrb","cq8tph2","cqmjyzt","cqft0i7","cqbw79j","cqkvzj6","cqchd1j","cqhhhxw","cq0h5iw","cq3pske","cqiiwi0"],"2010-04.csv":["c0p0hl3"],"2013-07.csv":["catu8rd","cb5wbqw","cb3ok6b","caxwi16","cbdb230"],"2010-12.csv":["c1a9awx"],"2012-05.csv":["c4l5589","c4t7wyk","c4ob0s1"],"2012-07.csv":["c5e1owf","c5gnbt6","c5cbpt6","c5hw588"],"2014-11.csv":["cmas3v7","clrtqg0","cma64o5","clwtjh7","cm4xum3","cm61wwn","clrj7rr","cmdv69u","cm27eme","clxj3k2","cmfhnhe","clquy0u","cmg7mn2","cmb45ca","clxmpae","cm2yb54"],"2014-09.csv":["ckbv6k4","ckbpzkk","ckbxp17","ckdhbsj","ckkymys","ckbppx5","ck93h70","ckmbf9b","ckawa31","ckkxm0p","ckj7ymw","ckp1lmx"],"2010-10.csv":["c1191tj","c12lr06"],"2012-06.csv":["c51vhw7","c4ut7xu","c55ffro","c4wecdb","c4wclri","c57fkut","c55d4ie"],"2013-10.csv":["ccnle38","cd0demh","cd15tna","cd16uj1","ccldm70","cctmryv","ccuwoc9","ccnd50t","cd3lj8h","ccjiom4","ccnzxok","ccy6lf9","ccjh7m7","ccngzdy"],"2011-11.csv":["c32cq8m","c31y0fg","c31e1dh","c30q4kh"],"2015-08.csv":["cu3lasu","cue6p3o","ctqgppm","cttwan9","cumcgq0","ctw098j","cuhrwe7","cty3m8q","cu0eqgx","cubknbn","ctohx2z","cu70oe0","cuaohhi","cu1h5ps","cu1x6bc","ctpi2qw"],"2013-01.csv":["c7pf3bq","c7uj4th","c7sac6i","c7r5dly","c804dbl","c7x9n04","c7yhb9p","c86rrlp","c80qp61","c864gmd","c7s4xdl","c7pe9zl","c7zladp","c7t4lih"],"2011-09.csv":["c2konue","c2hwbym"],"2012-12.csv":["c7ek6dd","c7flx0y","c7l2rl1","c7hbz05","c7ayof1"],"2012-02.csv":["c3uihm2","c3uh6xq","c3qeclg","c3tl06w"],"2014-06.csv":["cifuhar","ci2ufgh","ci8jla9","ciifiq5","ciaf7qw","chyitnf","ciezmzk","cib4dur"],"2009-07.csv":["c0bf05s"],"2014-02.csv":["cfn457p","cf4pq8s","cf8hpii","cfdqk7d","cfmmr5z","cfbu1bv","cfb7mq4","cf80hzs","cf5mdbq","cf8533s","cfew302"],"2012-09.csv":["c62f64t","c6921xn","c6207wb","c62ffov","c6eht8r","c62k2k9"],"2010-08.csv":["c0xd4zy"],"2014-08.csv":["cjj1bgn","cjnsdbh","cjmt720","cjlh5ug","cjnon8m"],"2011-02.csv":["c1ez2pc","c1h5xhf","c1h7y8x"],"2013-08.csv":["cbse0r6","cberhzn","cbsmi5k","cbh98j3","cbuwrkf","cbkgsjx","cbry1x9"],"2012-04.csv":["c48tjdc","c48asvj","c4bqbem"],"2012-11.csv":["c78dc7o","c6ytzed","c6v8rr2"],"2011-10.csv":["c2v6ryq","c2togi2"],"2009-08.csv":["c0bvh92","c0c58mf"],"2008-09.csv":["c05ijny"],"2010-06.csv":["c0sp4ih","c0sgj8h"],"2010-02.csv":["c0l4ty9"],"2012-03.csv":["c46kel7","c3wrf0m","c464gmo","c45ztny"],"2011-12.csv":["c37kdz6","c36fen1"],"2011-03.csv":["c1n0drw","c1jkkwk"],"2008-08.csv":["c0516u9","c050wns"],"2009-01.csv":["c078a50"],"2011-08.csv":["c2d7o7b"],"2011-01.csv":["c1bacn0"],"2010-03.csv":["c0lzd3p"],"2008-03.csv":["c03ehmx"],"2008-07.csv":["c04u58g"],"2011-06.csv":["c20naba"],"2008-05.csv":["c03yf4i"]}

filepath = os.popen('git rev-parse --show-toplevel').read().strip()

def generate_folds(dataset, labels, fold_count):
  folded = []
  for i in range(fold_count):
    folded.append({'test_set': [], 'train_set': [], 'test_labels': [], 'train_labels': []})
  i = 0
  all_counts = range(fold_count)
  for i in range(len(dataset)):
    mod = i%fold_count
    folded[mod]['test_set'].append(dataset[i])
    folded[mod]['test_labels'].append(labels[i])
    for c in all_counts:
      if c != mod:
        folded[c]['train_set'].append(dataset[i])
        folded[c]['train_labels'].append(labels[i])
  return folded

def merge_conmats(conmats):
  conmat = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
  for cc in conmats:
    for key in cc.keys():
      conmat[key] += cc[key]
  return conmat

def sensitivity(conmat):
  return float(conmat['tp'])/(conmat['tp']+conmat['fn'])

def specificity(conmat):
  return float(conmat['tn'])/(conmat['tn']+conmat['fp'])

def accuracy(conmat):
  return float(conmat['tn']+conmat['tp'])/sum(conmat.values())

def precision(conmat):
  return float(conmat['tp'])/(conmat['tp']+conmat['fp'])

def recall(conmat):
  return float(conmat['tp'])/(conmat['tp']+conmat['fn'])

def read_csv_str(filename):
  dataset = []
  i = 0
  with open(filename, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        dataset.append(row)
  return dataset

def generate_neural_net_sample_file_original(month_sets, labels):
  neural_net_dataset = []
  dataset_labels = []
  for month in month_sets.keys():
    print month
    for row in [r for r in read_csv_str(filepath+"/baumgartner_data/comments_altright/RC_"+month) if r[3] in month_sets[month]]:
      if (labels[row[3]] == 0.0 and np.random.random() < 0.25) or labels[row[3]] == 1.0:
        dataset_labels.append(labels[row[3]])
        neural_net_dataset.append(row)
  return neural_net_dataset, dataset_labels

def predictions_to_conmat(piped_model, fold, neural_net_votes, keyword_groups, vocab):
  conmat = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
  for guess, truth in zip(piped_model.predict(transform_raw_comments_to_expanded_features(fold['train_set'], neural_net_votes, keyword_groups, vocab)[0]), fold['test_labels']):
    if truth == 1 and guess > 0.5:
      conmat['tp'] += 1
    elif truth == 1 and guess < 0.5:
      conmat['fn'] += 1
    elif truth == 0 and guess < 0.5:
      conmat['tn'] += 1
    elif truth == 0 and guess > 0.5:
      conmat['fp'] += 1
  return conmat

class DenseTransformer(TransformerMixin):
  def transform(self, X, y=None, **fit_params):
    return X.todense()
  
  def fit_transform(self, X, y=None, **fit_params):
    self.fit(X, y, **fit_params)
    return self.transform(X)
  
  def fit(self, X, y=None, **fit_params):
    return self

def score_comment(comment):
  regular_expressions = ["(\(\(\(.*?\)\)\))",
  "(ethinic(|ity))",
  "(ethno(|-)state)",
  "(jew(|s))",
  "(goy(|s|im))",
  "(mexic(o|an))",
  "(rap(e|ing))",
  "(win(|ning))",
  "(iq)",
  "(jq)",
  "(joo(|s))",
  "(negro(|id|es))",
  "(caucasian(|s))",
  "(gene(|s|tics|otype|otypical))",
  "(slav(|ic))",
  "(hispanic(|s))",
  "(anti(|-)white(|ness))",
  "(radical(|ized))",
  "(gas chamber)",
  "(holocaust)",
  "(shoah(|ed))",
  "(hitler)",
  "(\/pol\/)",
  "(racial)",
  "(cancer(|ous))",
  "(cuck(|old|ed|y|ery|olding))",
  "(left(y|ies|ist))",
  "(asia(n|tic))",
  "(talmud(|ic))",
  "(trigger(y|ing|ed))",
  "(parasit(e|es|ic|ism))",
  "(immigra(nt|tion))",
  "(dindu)",
  "(dindu muffin)",
  "(dindu nuffin)",
  "(multicultural(|ism|ist))",
  "(skype)",
  "(specie(s|sism))",
  "(oven)",
  "(abo(|s))",
  "(shekel(|s))",
  "(libshit(|s))",
  "(fash(y|wave|ies))",
  "(white(|s|ness))",
  "(blm)",
  "(admixture)",
  "(alt(| |-)right)"]
  counts = []
  for regex in regular_expressions:
    counts.append(len(re.compile(regex, re.IGNORECASE).findall(comment)))
  return counts

#scores = [score_comment(r[5]) for r in dataset]
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", help="dataset to sanitize ('background' or 'inner')")
ap.add_argument("-t", "--test", help="is test? Add in option if it's a test otherwise leave empty")
ap.add_argument("-c", "--count", help="number of workers that will be used - default is 10", type=int, default=10)
args = vars(ap.parse_args())
args['dataset'] = 'inner'
prefix = '' if args["test"] == None else '_test'
filepath = os.popen('git rev-parse --show-toplevel').read().strip()
path = filepath+"/baumgartner_data"+prefix+"/machine_learning_resources"
results_path = filepath+"/baumgartner_data"+prefix+"/machine_learning_results"

keyword_groups = [set(el) for el in json.loads(open(filepath+"/baumgartner_data/machine_learning_resources/"+args["dataset"]+"_keyword_groups.json").read())]
researcher_labels = {}
for row in read_csv_str(filepath+"/baumgartner_data"+prefix+"/machine_learning_resources/"+args["dataset"]+"_researcher_votes.csv"):
  researcher_labels[row[0]] = float(row[1])

dataset, labels = generate_neural_net_sample_file_original(month_sets, researcher_labels)


models_used =  os.popen("ls "+path+"/"+args["dataset"]+"_neural_net_voter_*").read().split("\n")[:args["count"]]
datafiles = sorted(list(set(["missing_comments.csv"]).union(set([r.split("_")[-1] for r in os.popen("ls "+results_path).read().split("\n")]))-set(['', 'comments.csv'])))
all_data = {}
for month in datafiles:
  print month
  all_data[month] = [r[:-1] for r in read_csv_str(results_path+"/"+os.popen("ls "+results_path+" | grep "+month).read().split("\n")[0])]

model_results = {}
for i,model_used in enumerate(models_used):
  model_result = []
  print i
  for month in month_sets.keys():
    print "\t"+month
    if month == "missing_comments.csv":
      month_data = [r for r in read_csv_str(results_path+"/"+"dataset_"+args["dataset"]+"_model_"+str(i)+"_"+month) if r[3] in month_sets[month]]
    else: 
      month_data = [r for r in read_csv_str(results_path+"/"+"dataset_"+args["dataset"]+"_model_"+str(i)+"_RC_"+month) if r[3] in month_sets[month]]
    for row in month_data:
      if row[3] not in model_results.keys():
        model_results[row[3]] = []
      model_results[row[3]].append(float(row[-1]))

def transform_raw_comments_to_expanded_features(comment_data, neural_net_votes, keyword_groups, vocab=None):
  count_vect = None
  if vocab == None:
    count_vect = CountVectorizer()
  else:
    count_vect = CountVectorizer(vocabulary=vocab)
  X_counts = count_vect.fit_transform([r[5] for r in comment_data])
  tf_transformer = TfidfTransformer(use_idf=False).fit(X_counts)
  X_tfidf = tf_transformer.fit_transform(X_counts).todense().tolist()
  new_dataset = []
  comment_ids = []
  for ii,row in enumerate(X_tfidf):
    row.append(len(comment_data[ii][5]))
    parsed = set(re.split(ur"[\u200b\s]+", re.sub('[%s]' % re.escape(string.punctuation), ' ', comment_data[ii][5].lower()), flags=re.UNICODE))
    row.append(len(parsed))
    row.append(np.mean(neural_net_votes[comment_data[ii][3]]))
    row.append(np.mean(np.round(neural_net_votes[comment_data[ii][3]])))
    comment_ids.append(comment_data[ii][3])
    for kg in keyword_groups:
      row.append(len(kg.intersection(parsed)))
    for val in neural_net_votes[comment_data[ii][3]]:
      row.append(val)
    for count in score_comment(comment_data[ii][5]):
      row.append(count)
    row.append(sum(score_comment(comment_data[ii][5])))
    new_dataset.append(row)
  return new_dataset, comment_ids, count_vect.vocabulary_

avg_conmat = {"fp": 0, "tp": 0, "fn": 0, "tn": 0}
round_conmat = {"fp": 0, "tp": 0, "fn": 0, "tn": 0}
for key in researcher_labels.keys():
  if np.mean(neural_net_votes[key]) < 0.5 and researcher_labels[key] < 0.5:
    avg_conmat['tn'] += 1
  elif np.mean(neural_net_votes[key]) > 0.5 and researcher_labels[key] < 0.5:
    avg_conmat['fp'] += 1
  elif np.mean(neural_net_votes[key]) > 0.5 and researcher_labels[key] > 0.5:
    avg_conmat['tp'] += 1
  elif np.mean(neural_net_votes[key]) < 0.5 and researcher_labels[key] > 0.5:
    avg_conmat['fn'] += 1
  if np.mean(np.round(neural_net_votes[key])) < 0.5 and researcher_labels[key] < 0.5:
    round_conmat['tn'] += 1
  elif np.mean(np.round(neural_net_votes[key])) > 0.5 and researcher_labels[key] < 0.5:
    round_conmat['fp'] += 1
  elif np.mean(np.round(neural_net_votes[key])) > 0.5 and researcher_labels[key] > 0.5:
    round_conmat['tp'] += 1
  elif np.mean(np.round(neural_net_votes[key])) < 0.5 and researcher_labels[key] > 0.5:
    round_conmat['fn'] += 1

row.append()
row.append()

folds = generate_folds(dataset, labels, 10)
conmats = []
for piped_model in models:
  fold_conmats = []
  for fold in [folds[1]]:
    transformed_dataset, comment_ids, vocab = transform_raw_comments_to_expanded_features(fold['train_set'], neural_net_votes, keyword_groups)
    piped_model.fit(transformed_dataset, fold['train_labels'])
    fold_conmats.append(predictions_to_conmat(piped_model, fold, neural_net_votes, keyword_groups, vocab))
    print fold_conmats
  conmats.append(merge_conmats(fold_conmats))

best_model = models[[accuracy(c) for c in conmats].index(sorted([accuracy(c) for c in conmats])[-1])]
piped_model = Pipeline([('vect', CountVectorizer(stop_words='english', strip_accents='unicode', ngram_range=(1,3))),
  ('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
  ('to_dense', DenseTransformer()), 
  ('clf', best_model)])

print "Best Fitting Model for Dataset is:"
print best_model
mapped_guesses = {}
fold_conmats = []
for fold in folds:
  best_model.fit(fold['train_set'], [f[0] for f in fold['train_labels']])
  predictions = zip(fold['test_labels'], best_model.predict(fold['test_set']))
  conmat = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
  vals = []
  i = 0
  for label_data, prediction in predictions:
    val = None
    if prediction < 0.5:
      val = 0
    else:
      val = 1
    if val == 0 and label_data[0] < 0.5:
      conmat['tn'] += 1
    elif val == 0 and label_data[0] > 0.5:
      conmat['fn'] += 1
    elif val == 1 and label_data[0] < 0.5:
      conmat['fp'] += 1
    elif val == 1 and label_data[0] > 0.5:
      conmat['tp'] += 1
    vals.append(val)
    mapped_guesses[label_data[1]] = val
    i += 1
  fold_conmats.append(conmat)

print "merge_conmats(fold_conmats)"
print merge_conmats(fold_conmats)
print "sensitivity(merge_conmats(fold_conmats))"
print sensitivity(merge_conmats(fold_conmats))
print "specificity(merge_conmats(fold_conmats))"
print specificity(merge_conmats(fold_conmats))
print "accuracy(merge_conmats(fold_conmats))"
print accuracy(merge_conmats(fold_conmats))
print "precision(merge_conmats(fold_conmats))"
print precision(merge_conmats(fold_conmats))
print "recall(merge_conmats(fold_conmats))"
print recall(merge_conmats(fold_conmats))

correct = 0
for k in mapped_guesses.keys():
  if researcher_labels[k] == mapped_guesses[k]:
    correct += 1