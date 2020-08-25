import os
import sys
import cv2
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
	
	def run_tests(json_files: str) -> dict:
		# check dictionary of data
		for key, value in data.items():
			if key in words:
				pretty(key, words[key])
				sys.exit(f"[\u2718] Duplicate key '{key}' found in file {file_path}.")
		
		# check if wordlist is sorted
		pairs = []
		keys = get_wordlist(data)
		for i in range(1, len(keys)):
			if keys[i - 1] > keys[i]:
				pairs.append([keys[i - 1], keys[i]])
		if pairs:
			print(pairs)
			sys.exit(f'[\u2718] Wordlist is not sorted for file {file_path}.')
		
		# check if image is present
		images = set(os.listdir(os.path.join(base_dir, 'images')))
		original = set(os.listdir(os.path.join(base_dir, 'original')))
		no_image = []
		for key, value in data.items():
			found = False
			for i in range(len(value)):
				if value[i]['image'] in images and value[i]['image'] in original:
					found = True
			if not found:
				no_image.append(key)
		if no_image:
			print(no_image)
			sys.exit(f'[\u2718] Incorrect path to images for file {file_path}.')
		
		# check if images are square
		not_square = []
		for img_path in images:
			img = cv2.imread(os.path.join(base_dir, 'images', img_path))
			height, width, _ = img.shape
			if height != width:
				not_square.append([img_path, height, width])
		if not_square:
			print(not_square)
			sys.exit(f'[\u2718] Not square images found for file {file_path}.')
		
		# print(f'Processed {file_path}.')
	
	
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



def search(word: str, data: dict) -> bool:
	similar = []
	size = min(5, len(word))
	
	# loop over the word list
	for key, value in data.items():
		if key == word:
			pretty(key, value)
			print(f'The word was found.')
			return True
		elif key[:size] == word[:size]:
			similar.append([key, value])
	
	print(f'The word {args.word} was not found.')
	
	# found similar words
	if similar:
		print('Possible matches:')
		for key, value in similar:
			pretty(key, value)
	
	return False



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
	
	# search for word in wordlist
	if args.word:
		search(args.word, data)
	
	print('[\u2714] All checks passed!')