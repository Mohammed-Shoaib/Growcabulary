import os
import re
import sys
import time
import json
import regex
import shutil
import argparse
import requests

from utils import *
from typing import List
from selenium import webdriver
from urllib.parse import urljoin
from urllib.request import FancyURLopener
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# global variables
base_url = 'https://dictionary.cambridge.org/dictionary/english/'



def extract_wiki(link: str) -> None:
	name = os.path.basename(os.path.normpath(link))
	name = re.sub(r'^\d+px-', r'', name)
	print()
	url = f'https://commons.wikipedia.org/wiki/File:{name}'
	print(url)



def download_audio(url: str, path: str) -> None:
	if not url:
		return
	r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
	with open(path, 'wb') as f:
		f.write(r.content)



def get_phonetic(driver, class_name: str) -> str:
	# extract key
	title = driver.find_elements_by_class_name('di-title')
	if not title:
		return ["", "", ""]
	key = title[0].text.strip()
	
	# extract the pronunciation
	ele = driver.find_elements_by_class_name(class_name)
	if not ele:
		print(f'{key} not found, phonetic error.')
		return ["", "", key]
	ele = ele[0]
	span = ele.find_elements_by_tag_name('span')
	if len(span) < 3:
		print(f'{key} not found, phonetic length error.')
		return ["", "", key]
	phonetic = span[2].text.strip()
	
	# extract audio
	sources = ele.find_elements_by_tag_name('audio')
	if sources:
		html = sources[0].get_attribute('innerHTML')
		audio = re.search(r'src="(.*mp3)"', html).group(1)
		if not audio.startswith('http'):
			audio = urljoin(base_url, audio)
	else:
		audio = ''
		print(f'{key} not found, audio error.')
	
	return [phonetic, audio, key]



def found_phonetics(value: List[dict]) -> bool:
	for v in value:
		if v['image']:
			return 'phonetics-us' in v and 'phonetics-uk' in v
	return False



def scrape_phonetic() -> None:
	cnt = length = 0
	file_name = 'phonetics.json'
	driver = webdriver.Firefox()
	
	with open('mapping_cambridge.json', 'r') as f:
		mapping = json.load(f)
	
	with open(file_name, 'r') as f:
		phonetics = json.load(f)
	
	for key, value in data.items():
		if not found_phonetics(value) and key not in phonetics:
			length += 1
	
	for key, value in data.items():
		if found_phonetics(value) or key in phonetics:
			continue
		cnt += 1
		
		# load page
		url = urljoin(base_url, key)
		r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
		code = r.status_code
		driver.get(url)
		
		# error handle 404
		if base_url == driver.current_url or code != 200:
			print(f'{key} not found, status code: {code}.')
			continue
		
		# get phonetic pronunciation
		uk = get_phonetic(driver, "uk")
		us = get_phonetic(driver, "us")
		
		# error handle incorrect word
		k = mapping[key] if key in mapping else key
		if k != us[2]:
			print(f'{key} not found, incorrect word: {us[2]}')
			continue
		if not us[0] or not uk[0]:
			continue
		
		# save data in phonetics
		phonetics[key] = {}
		phonetics[key]['uk'] = uk[0]
		phonetics[key]['us'] = us[0]
		download_audio(uk[1], f'audio/{key}-uk.mp3')
		download_audio(us[1], f'audio/{key}-us.mp3')
		
		with open(file_name, 'w', encoding='utf8') as f:
			json.dump(phonetics, f, indent=4, ensure_ascii=False)
		
		print(f'Finished {cnt} out of {length}.', file=sys.stderr)



# add keyword arguments
parser = argparse.ArgumentParser()
parser.add_argument('--wiki', '-w', help="The upload wikipedia link", type=str)
parser.add_argument('--phonetic', '-p', help="Scrape the phonetics of word", action='store_true')
parser.add_argument('--tests', '-t', help="Run tests", action='store_true')
args = parser.parse_args()



if __name__ == '__main__':
	# load data
	data = get_data(args.tests)
	
	if args.wiki:
		extract_wiki(args.wiki)
	if args.phonetic:
		scrape_phonetic()