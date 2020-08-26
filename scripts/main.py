import os
import sys
import cv2
import json
import shutil
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



def remove(word: str, data: dict):
	search(word, data)
	
	for ele in data[word]:
		if ele['image']:
			file_name, ext = os.path.splitext(ele['image'])
			break
	
	img = os.path.join(data[word][0]['path'], 'images', f'{word}{ext}')
	org = os.path.join(data[word][0]['path'], 'original', f'{word}{ext}')
	
	if os.path.exists(img):
		os.remove(img)
	if os.path.exists(org):
		os.remove(org)
	
	print('Deleted image successfully!')



def copy(src: str, dst: str, data: dict):
	if not args.dst:
		sys.exit(f'[\u2718] No destination word specified!')
	search(src, data)
	search(dst, data)
	
	for ele in data[src]:
		if ele['image']:
			file_name, ext = os.path.splitext(ele['image'])
			break
	
	img_src = os.path.join(data[src][0]['path'], 'images', f'{src}{ext}')
	org_src = os.path.join(data[src][0]['path'], 'original', f'{src}{ext}')
	
	if not os.path.exists(img_src):
		sys.exit(f'[\u2718] The path to the source image {img_src} does not exist.')
	elif not os.path.exists(org_src):
		sys.exit(f'[\u2718] The path to the source original {org_src} does not exist.')
	
	img_dst = os.path.join(data[dst][0]['path'], 'images', f'{dst}{ext}')
	org_dst = os.path.join(data[dst][0]['path'], 'original', f'{dst}{ext}')
	
	shutil.copy(img_src, img_dst)
	shutil.copy(org_src, org_dst)
	
	print(f'File extension: {ext}')
	print('Copied image successfully!')



def is_image(path: str):
	_, ext = os.path.splitext(path)
	return ext in ['.jpg', '.jpeg', '.png']



def save(path: str, data: dict):
	if not os.path.exists(path):
		sys.exit(f'[\u2718] The path to moves images {path} does not exist.')
	
	downloads = os.path.expanduser('~/Downloads')
	files = filter(is_image, os.listdir(downloads))
	
	for f in files:
		file_name, ext = os.path.splitext(f)
		
		if file_name.endswith(' (1)'):
			name = file_name.replace(' (1)', '')
			dst = os.path.join(path, 'images', f'{name}{ext}')
		else:
			dst = os.path.join(path, 'original')
		
		src = os.path.join(downloads, f)
		shutil.move(src, dst)
		
		print(f'Successfully moved {file_name} with extension {ext}')
	


# add keyword arguments
parser = argparse.ArgumentParser()
parser.add_argument('--word', '-w', help="The word to search", type=str.lower)
parser.add_argument('--remove', '-r', help="The word to remove", type=str.lower)
parser.add_argument('--src', '-src', help="The source word to copy from", type=str.lower)
parser.add_argument('--dst', '-dst', help="The destination word to copy to", type=str.lower)
parser.add_argument('--tests', '-t', help="Run tests", action='store_true')
parser.add_argument('--save', '-s', help="The folder to save words from the downloads folder", type=str)
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
	
	# remove image for word
	if args.remove:
		remove(args.remove, data)
	
	# copy image from source word to destination word
	if args.src:
		copy(args.src, args.dst, data)
	
	# moves files from the downloads folder and saves them
	if args.save:
		save(args.save, data)
	
	print('[\u2714] All checks passed!')