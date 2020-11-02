import os
import sys
import shutil
import argparse

from utils import *



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
	
	# found similar words
	if similar:
		print('Possible matches:')
		for key, value in similar:
			pretty(key, value)
	
	print(f'The word {args.word} was not found.')
	
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
		if os.path.exists(os.path.join(dst, f)):
			os.remove(os.path.join(dst, f))
		shutil.move(src, dst)
		
		print(f'Successfully moved {file_name} with extension {ext}')



def sort_words(path: str) -> None:
	path = os.path.join(path, 'data.json')
	with open(path, 'r') as f:
		data = json.load(f)
	format_json(data, path, sort_keys=True)



# add keyword arguments
parser = argparse.ArgumentParser()
parser.add_argument('--word', '-w', help="The word to search", type=str)
parser.add_argument('--remove', '-r', help="The word to remove", type=str)
parser.add_argument('--src', '-src', help="The source word to copy from", type=str)
parser.add_argument('--dst', '-dst', help="The destination word to copy to", type=str)
parser.add_argument('--tests', '-t', help="Run tests", action='store_true')
parser.add_argument('--save', '-s', help="The folder to save words from the downloads folder", type=str)
parser.add_argument('--sort', '-ss', help="The path to the folder of the word list to sort", type=str)
args = parser.parse_args()



if __name__ == '__main__':
	# load data
	data = get_data(args.tests)
	
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
	
	# sorts the json file in the word list
	if args.sort:
		sort_words(args.sort)