import os
import re
import argparse

from utils import *



# global variables
base_url = 'https://dictionary.cambridge.org/dictionary/english/'



def extract_wiki(link: str) -> None:
	name = os.path.basename(os.path.normpath(link))
	name = re.sub(r'^\d+px-', r'', name)
	print()
	url = f'https://commons.wikipedia.org/wiki/File:{name}'
	print(url)



# add keyword arguments
parser = argparse.ArgumentParser()
parser.add_argument('--wiki', '-w', help="The upload wikipedia link", type=str)
parser.add_argument('--tests', '-t', help="Run tests", action='store_true')
args = parser.parse_args()



if __name__ == '__main__':
	# load data
	data = get_data(args.tests)
	
	if args.wiki:
		extract_wiki(args.wiki)