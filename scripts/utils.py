import os
import sys
import cv2
import json
import regex

from typing import List
from pathlib import Path
from pprint import pprint
from unidecode import unidecode
from collections import defaultdict, OrderedDict



# global variables
root_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
folders = ['Common', 'Basic', 'Advanced', 'PrepScholar', 'Barron']		# ['Personal']



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



def normalize(s: str) -> str:
	return unidecode(s.lower())



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



def update_stats(files: List[str], data: dict) -> None:
	total = 0
	freq = defaultdict(int)
	files = [Path(f).parent.name for f in files]
	
	for key, value in data.items():
		folder = Path(value[0]['path']).name
		freq[folder] += 1
		total += 1
	freq['Total'] = total
	
	dir_name = os.path.join(os.path.dirname(os.path.realpath(__file__)))
	path = os.path.join(dir_name, '..', 'assets', 'stats.json')
	with open(path, 'w') as f:
		json.dump(freq, f, indent=4)



def format_json(data: dict, path: str, sort_keys=False):
	if sort_keys:
		data = OrderedDict(sorted(data.items()))
	
	with open('temp.json', 'w', encoding='utf8') as f:
		json.dump(data, f, indent='\t', ensure_ascii=False)
	
	with open('temp.json', 'r') as f:
		content = f.read()
	os.remove('temp.json')
	
	# ws denotes whitespace
	# remove the square bracket [ws] curly bracket
	content = regex.sub(r'\[\n\s*\{', '[{', content)
	content = regex.sub(r'\}\n\s*\]', '}]', content)
	
	# ! only works for \w characters
	# remove the [ [ws] "words", ] [[ws]w1,[ws]w2,[ws]w3] => [w1,w2,w3]
	content = regex.sub(r'(?<=\[((\n\s+)?"\w+",)*)\n\s+"', '"', content)
	content = regex.sub(r'(?<=",?)\n\s+(?=("\w+",?(\n\s+)?)*\])', '', content)
	
	# add space between words in array [w1,w2,w3] => [w1, w2, w3]
	content = regex.sub(r'(?<="\w+",)"', ' "', content)
	
	# change 3 tab spaces to 2 tab spaces
	content = regex.sub(r'\t{3}', '\t\t', content)
	
	# remove nesting tab spaces for curly brackets
	content = regex.sub(r'\t{2}(?=\})', '\t', content)
	
	# change } [ws] { => }, {
	content = regex.sub(r'\},\n\s+\{', '}, {', content)
	
	with open(path, 'w') as f:
		f.write(content)



def get_data(is_test: bool = False) -> dict:
	words = {}
	passed = True
	json_files = []
	
	# traverse all the files in root directory
	for root, dirs, files in os.walk(root_dir):
		if Path(root).parent != Path(root_dir):
			continue
		for f in files:
			if f.endswith('.json') and any(folder in root for folder in folders):
				json_files.append(os.path.join(root, f))
	
	# get the wordlist
	json_files.sort(key = lambda x: [folders.index(Path(x).parent.name.split()[0]), x])


	def run_tests(data: dict, file_path: str) -> None:
		nonlocal passed
		is_fast = True
		
		# skip the tests involving images if personal word list
		personal = Path(file_path).parent.name.split()[0] == 'Personal'
		
		# check dictionary of data
		for key, value in data.items():
			if key in words:
				passed = False
				pretty(key, words[key])
				print(f"[\u2718] Duplicate key '{key}' found in file {file_path}.", file=sys.stderr)
		
		# check if all properties are present
		not_present = []
		for key, value in data.items():
			for v in value:
				if not all(x in v for x in ['pos', 'def', 'synonyms', 'antonyms', 'alternatives', 'image', 'notes', 'examples', 'website']):
					not_present.append(key)
					break
		if not_present:
			passed = False
			print(not_present)
			print(f'[\u2718] Wordlist does not contain all the properties for file {file_path}.', file=sys.stderr)
		
		# check if wordlist is sorted
		pairs = []
		keys = get_wordlist(data)
		for i in range(1, len(keys)):
			k1, k2 = normalize(keys[i - 1]), normalize(keys[i])
			if k1 > k2:
				pairs.append([k1, k2])
		if pairs:
			passed = False
			print(pairs)
			print(f'[\u2718] Wordlist is not sorted for file {file_path}.', file=sys.stderr)
		
		if is_fast:
			print(f'Processed {Path(file_path).parent.name}.')
			return
		
		# check if pos is correct
		wrong_pos = []
		for key, value in data.items():
			for v in value:
				if v['pos'] not in ['noun', 'adjective', 'verb', 'adverb']:
					wrong_pos.append(key)
		if wrong_pos:
			passed = False
			print(wrong_pos)
			print(f'[\u2718] Wrong pos found for file {file_path}.', file=sys.stderr)
		
		# check if image, link, and phonetic is present
		images = os.listdir(os.path.join(base_dir, 'images'))
		original = os.listdir(os.path.join(base_dir, 'original'))
		no_image = []
		no_link = []
		no_phonetics = []
		seen_images = []
		for key, value in data.items():
			found = False
			for i in range(len(value)):
				img_path = value[i]['image']
				if img_path:
					if img_path not in images or img_path not in original:
						no_image.append(key)
					if not value[i]['website']:
						no_link.append(key)
					if not value[i]['phonetics-us'] or not value[i]['phonetics-uk']:
						no_phonetics.append(key)
					seen_images.append(img_path)
					found = True
			if not found:
				no_image.append(key)
		if no_image and not personal:
			passed = False
			print(no_image)
			print(f'[\u2718] Incorrect path to images for file {file_path}.', file=sys.stderr)
		if no_link and not personal:
			passed = False
			print(no_link)
			print(f'[\u2718] No website for images specified for file {file_path}.', file=sys.stderr)
		if no_phonetics:
			passed = False
			print(no_phonetics)
			print(f'[\u2718] No phonetics specified for file {file_path}.', file=sys.stderr)
		
		# check if audio files are present
		audios = os.listdir(os.path.join(base_dir, 'audio'))
		no_audio = []
		seen_audio = []
		for key, value in data.items():
			audio = [f'{key}-us.mp3', f'{key}-uk.mp3']
			if any(x not in audios for x in audio):
				no_audio.append(key)
			seen_audio.extend(audio)
		if no_audio:
			passed = False
			print(no_audio)
			print(f'[\u2718] No phonetic audio pronunciation found for file {file_path}.', file=sys.stderr)
		
		# check if images are square
		not_square = []
		for img_path in images:
			img = cv2.imread(os.path.join(base_dir, 'images', img_path))
			height, width, _ = img.shape
			if height != width:
				not_square.append([img_path, height, width])
		if not_square and not personal:
			passed = False
			print(not_square)
			print(f'[\u2718] Not square images found for file {file_path}.', file=sys.stderr)
		
		# check if image has the same name as the key
		not_same_key = []
		keys = set(img.rsplit('.', 1) for img in images)
		for key, _ in data.items():
			if key not in keys:
				not_same_key.append(key)
		if not_same_key:
			passed = False
			print(not_same_key)
			print(f'[\u2718] Not same key images found for file {file_path}.', file=sys.stderr)
		
		# check if additional images files present
		extra_img = []
		for image in images:
			file_name, ext = os.path.splitext(image)
			file_name = Path(file_name).name + ext
			if file_name not in seen_images:
				extra_img.append(image)
		if extra_img:
			passed = False
			print(extra_img)
			print(f'[\u2718] Additional square images found in {file_path}.', file=sys.stderr)
		
		# check if additional original files present
		extra_org = []
		for image in original:
			file_name, ext = os.path.splitext(image)
			file_name = Path(file_name).name + ext
			if file_name not in seen_images:
				extra_org.append(image)
		if extra_org:
			passed = False
			print(extra_org)
			print(f'[\u2718] Additional original images found in {file_path}.', file=sys.stderr)
		
		# check if additional audio files present
		extra_audio = []
		for audio in audios:
			file_name, ext = os.path.splitext(audio)
			file_name = Path(file_name).name + ext
			if file_name not in seen_audio:
				extra_audio.append(audio)
		if extra_audio:
			passed = False
			print(extra_audio)
			print(f'[\u2718] Additional audio files found in {file_path}.', file=sys.stderr)
		
		print(f'Processed {Path(file_path).parent.name}.')
	
	
	# read each json file
	for file_path in json_files:
		# read contents as json
		base_dir = Path(file_path).parent
		with open(file_path, 'r') as f:
			try:
				data = json.load(f, object_pairs_hook=dict_raise_on_duplicates)
			except ValueError as e:
				passed = False
				print(f"[\u2718] Duplicate key '{e}' found in file {file_path}.", file=sys.stderr)
		
		# ! removes empty keys
		# data = {key: value for key, value in data.items() if key}
		
		# add attribute 'path' to each element
		for key, value in data.items():
			for i in range(len(value)):
				value[i]['path'] = base_dir
		
		# run tests
		if is_test:
			run_tests(data, file_path)
		
		# extend dictionary with new data
		words.update(data)
	
	if is_test:
		if passed:
			print('[\u2714] All checks passed!', file=sys.stderr)
			update_stats(json_files, words)
		else:
			print('[\u2718] Failed to pass all checks!', file=sys.stderr)
	
	return words