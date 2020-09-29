import os
import sys
import cv2
import json

from typing import List
from pathlib import Path
from pprint import pprint



# global variables
root_dir = '/home/shoaib/Desktop/GREPrep/'
folders = ['Common', 'Basic', 'Advanced']



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



def is_image(path: str):
	_, ext = os.path.splitext(path)
	return ext in ['.jpg', '.jpeg', '.png']



def load_image(path: str):
	# read image with alpha channels
	img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
	
	# convert transparent to white background
	if len(img.shape) == 3 and img.shape[2] == 4:
		trans_mask = img[:, :, 3] == 0
		img[trans_mask] = [255, 255, 255, 255]
		img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
	
	return img



def get_wordlist(data: dict) -> List[str]:
	return list(data.keys())



def get_data(is_test: bool = False) -> dict:
	words = {}
	json_files = []
	
	# traverse all the files in root directory
	for root, dirs, files in os.walk(root_dir):
		for f in files:
			if f.endswith('.json') and any(folder in root for folder in folders):
				json_files.append(os.path.join(root, f))
	
	# get the wordlist
	json_files.sort(key = lambda x: [folders.index(Path(x).parent.name.split()[0]), x])


	def run_tests(data: dict) -> None:
		# check dictionary of data
		for key, value in data.items():
			if key in words:
				pretty(key, words[key])
				sys.exit(f"[\u2718] Duplicate key '{key}' found in file {file_path}.")
		
		# check if wordlist is sorted
		pairs = []
		keys = get_wordlist(data)
		for i in range(1, len(keys)):
			k1, k2 = keys[i - 1].lower(), keys[i].lower()
			if k1 > k2:
				pairs.append([k1, k2])
		if pairs:
			print(pairs)
			sys.exit(f'[\u2718] Wordlist is not sorted for file {file_path}.')
		
		# check if image is present
		images = os.listdir(os.path.join(base_dir, 'images'))
		original = os.listdir(os.path.join(base_dir, 'original'))
		no_image = []
		for key, value in data.items():
			found = False
			for i in range(len(value)):
				img_path = value[i]['image']
				if img_path:
					if img_path not in images or img_path not in original:
						no_image.append(key)
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
		
		# check if additional files present
		extra_img = []
		extra_org = []
		for image in images:
			file_name, ext = os.path.splitext(image)
			if file_name not in data:
				extra_img.append(image)
		if extra_img:
			print(extra_img)
			sys.exit(f'[\u2718] Additional square images found in {file_path}.')
		for image in original:
			file_name, ext = os.path.splitext(image)
			if file_name not in data:
				extra_org.append(image)
		if extra_org:
			print(extra_org)
			sys.exit(f'[\u2718] Additional original images found in {file_path}.')
		
		print(f'Processed {file_path}.')
	
	
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
		if is_test:
			run_tests(data)
		
		# extend dictionary with new data
		words.update(data)
	
	if is_test:
		print('[\u2714] All checks passed!')
	
	return words