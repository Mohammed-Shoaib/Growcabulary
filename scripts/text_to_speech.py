import os
import time
import argparse

from utils import *
from gtts import gTTS
from pydub import AudioSegment



def convert_text_to_speech(data: dict) -> None:
	os.makedirs('import', exist_ok=True)
	for key, value in data.items():
		folder = os.path.basename(os.path.normpath(value[0]['path']))
		print(f'Processing word {key} from {folder}...')
		
		for i, v in enumerate(value):
			os.makedirs(f'import/{key}', exist_ok=True)
			file_path = f'import/{key}/def-{i + 1}.mp3'
			while not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
				try:
					tts = gTTS(text=v['def'], lang='en', slow=False)
					tts.save(file_path)
				except Exception as e:
					print(f'Failed tts for {key}, trying again...')



def save_text_to_speech(data: dict) -> None:
	os.makedirs('export', exist_ok=True)
	for key, value in data.items():
		folder = os.path.basename(os.path.normpath(value[0]['path']))
		print(f'Processing word {key} from {folder}...')
		
		base = value[0]['path']
		audio = AudioSegment.empty()
		audio += AudioSegment.from_mp3(os.path.join(base, 'audio', f'{key}-us.mp3'))
		
		for i, v in enumerate(value):
			audio += AudioSegment.silent(duration=2000)
			audio += AudioSegment.from_mp3(f'import/{v["pos"]}.mp3')
			audio += AudioSegment.from_mp3(f'import/{key}/def-{i + 1}.mp3')
		
		os.makedirs(os.path.join('export', folder), exist_ok=True)
		audio.export(os.path.join('export', folder, f'{key}.mp3'), format='mp3')



# add keyword arguments
parser = argparse.ArgumentParser()
parser.add_argument('--convert', '-c', help="Convert text to speech", action='store_true')
parser.add_argument('--save', '-s', help="Save the audio into a neat organized file", action='store_true')
args = parser.parse_args()

if __name__ == '__main__':
	data = get_data()
	
	if args.convert:
		convert_text_to_speech(data)
	if args.save:
		save_text_to_speech(data)