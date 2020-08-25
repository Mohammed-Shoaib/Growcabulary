import os
import sys
import json
import argparse

from typing import List
from pathlib import Path
from pprint import pprint



def dict_raise_on_duplicates(ordered_pairs):
	""" Raises an error for duplicate keys """
	d = {}
	for k, v in ordered_pairs:
		if k in d and k != "":	# ! ignores empty keys
		   raise ValueError(k)
		else:
		   d[k] = v
	return d



def pretty(key, value):
	print(f'{key}: ', end='')
	pprint(value)



def get_data(data: dict):
	words = {}
	
	# read each json file
	for file_path in json_files:
		# read contents as json
		base_dir = Path(file_path).parent
		with open(file_path, 'r') as f:
			try:
				data = json.load(f, object_pairs_hook=dict_raise_on_duplicates)
			except ValueError as e:
				sys.exit(f"[\u2718] Duplicate key '{e}' found in file {file_path}.")
		
		# ! removes empty keys
		# data = {key: value for key, value in data.items() if key}
		
		# add attribute 'path' to each element
		for key, value in data.items():
			for i in range(len(value)):
				value[i]['path'] = base_dir
		
		# run tests
		if args.tests:
			run_tests(data)
		
		# extend dictionary with new data
		words.update(data)
	
	return words



def get_wordlist(data: dict) -> List[str]:
	return list(data.keys())



# add keyword arguments
parser = argparse.ArgumentParser()
parser.add_argument('--word', '-w', help="The word to search", type=str.lower)
parser.add_argument('--src', '-src', help="The source word to copy from", type=str.lower)
parser.add_argument('--dst', '-dst', help="The destination word to copy to", type=str)
parser.add_argument('--tests', '-t', help="Run tests", action='store_true')
args = parser.parse_args()



if __name__ == '__main__':
	base_dir = '../'
	json_files = []
	
	# traverse all the files in root directory
	folders = ['Common', 'Basic', 'Advanced']
	for root, dirs, files in os.walk(base_dir):
		for f in files:
			if f.endswith('.json') and any(folder in root for folder in folders):
				json_files.append(os.path.join(root, f))
	
	# get the wordlist
	json_files.sort()
	data = get_data(json_files)