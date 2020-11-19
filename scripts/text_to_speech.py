import os
import time
import argparse

from utils import *
from gtts import gTTS
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC



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
		# initialization
		base = value[0]['path']
		folder = os.path.basename(os.path.normpath(base))
		file_name = os.path.join('export', folder, f'{key}.mp3')
		
		print(f'Processing word {key} from {folder}...')
		
		# create the audio file
		audio = AudioSegment.empty()
		audio += AudioSegment.from_mp3(os.path.join(base, 'audio', f'{key}-us.mp3'))
		audio += AudioSegment.silent(duration=3000)
		
		for i, v in enumerate(value):	
			audio += AudioSegment.from_mp3(f'import/{v["pos"]}.mp3')
			audio += AudioSegment.from_mp3(f'import/{key}/def-{i + 1}.mp3')
			audio += AudioSegment.silent()
		
		# save the audio file
		os.makedirs(Path(file_name).parent, exist_ok=True)
		audio.export(file_name, format='mp3')
		
		# check if image is present
		img_path = ''
		for v in value:
			if v['image'] and os.path.exists(os.path.join(base, 'images', v['image'])):
				img_path = os.path.join(base, 'images', v['image'])
		if not img_path:
			print(f'[\u2718] Path to image does not exist for {key} in {folder}.', file=sys.stderr)
			continue
		ext = os.path.splitext(img_path)[1]
		
		# add the album art
		audio = MP3(file_name, ID3=ID3)
		audio.tags.add(APIC(
			encoding=3, # 3 is for utf-8
			mime='image/png' if ext == 'png' else 'image/jpeg',
			type=3, # 3 is for the cover image
			desc=key,
			data=open(img_path, 'rb').read()
		))
		audio.save()
		



# add keyword arguments
parser = argparse.ArgumentParser()
parser.add_argument('--convert', '-c', help="Convert text to speech", action='store_true')
parser.add_argument('--save', '-s', help="Save the audio into a neat organized file", action='store_true')
args = parser.parse_args()

if __name__ == '__main__':
	data = get_data()
	
	for key, value in list(data.items()):
		# check if definition exists
		skip = False
		for v in value:
			if not v['pos'] or not v['def']:
				skip = True
		if skip:
			print(f'[\u2718] Definition missing for {key} present in {value[0]["path"]}.', file=sys.stderr)
			del data[key]
	
	if args.convert:
		convert_text_to_speech(data)
	if args.save:
		save_text_to_speech(data)