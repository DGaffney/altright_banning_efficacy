import pickle
import csv
import argparse
from os import listdir
from os.path import isfile, join
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", help="file to learn from")
args = vars(ap.parse_args())
model = pickle.loads(open("ml_model_altright.pkl").read())
