import io
import cv2

from utils import *
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping



def data_to_pdf(data: dict) -> None:
	# register required fonts
	pdfmetrics.registerFont(TTFont('Lato-Regular', 'Lato-Regular.ttf'))
	pdfmetrics.registerFont(TTFont('Lato-Bold', 'Lato-Bold.ttf'))
	pdfmetrics.registerFont(TTFont('Lato-Italic', 'Lato-Italic.ttf'))
	pdfmetrics.registerFont(TTFont('Lato-SemiBold', 'Lato-SemiBold.ttf'))
	pdfmetrics.registerFont(TTFont('Lato-BoldItalic', 'Lato-BoldItalic.ttf'))
	
	# to use <b> or <strong> and <i> or <em> tags
	# 2nd param is for boldface and 3rd param is for italic
	addMapping('Lato-Regular', 0, 0, 'Lato-Regular')
	addMapping('Lato-Regular', 0, 1, 'Lato-Italic')
	addMapping('Lato-Regular', 1, 0, 'Lato-SemiBold')
	addMapping('Lato-Regular', 1, 1, 'Lato-BoldItalic')
	
	# initialization
	width, height = 8.5 * inch, 11 * inch
	idx, mod = -1, 3
	img_dim = 200
	text_width, text_height = width - img_dim - 150, height // 3
	text_start = img_dim + inch / 1.5
	start, center = height, width / 2
	line_offset, word_offset = 14, 20
	heading_size, regular_size = 24, 13
	
	# create an empty canvas
	dir_name = os.path.join(os.path.dirname(os.path.realpath(__file__)))
	path = os.path.join(dir_name, '..', 'assets', 'Growcabulary.pdf')
	canvas = Canvas(path)
	
	def next_word():
		nonlocal idx, start
		idx += 1
		if idx == mod:
			idx = 0
			canvas.showPage()
		start = height - idx * height / 3
	
	def next_line(offset):
		nonlocal start
		start -= offset
	
	import time
	beg = time.time()
	prev = ""
	for key, value in data.items():
		next_word()
		folder = os.path.basename(os.path.normpath(value[0]['path']))
		personal = folder.split()[0] == 'Personal'
		print(f'Processing word {key} from {folder}...')
		
		if prev != folder:
			if idx != 0:
				canvas.showPage()
			idx = -1
			next_word()
			prev = folder
			canvas.setFont('Lato-Regular', heading_size)
			canvas.drawCentredString(center, height + 20, folder)
		
		# the word
		style = ParagraphStyle(name='key', fontName='Lato-Bold', fontSize=regular_size)
		para = Paragraph(key, style)
		w, h = para.wrap(text_width, text_height)
		para.drawOn(canvas, text_start, start)
		
		for val in value:
			if val['image']:
				phonetics = [val['phonetics-us'][0], val['phonetics-uk'][0]]
		
		# phonetics
		style = ParagraphStyle(name='phonetics', fontName='Lato-Regular', fontSize=regular_size)
		para = Paragraph(f'US {phonetics[0]}{"&nbsp;" * 8}UK {phonetics[1]}', style)
		w, h = para.wrap(text_width, text_height)
		next_line(h)
		para.drawOn(canvas, text_start, start)
		
		for i, val in enumerate(value):
			# the part of speech
			style = ParagraphStyle(name='pos', fontName='Lato-BoldItalic', fontSize=regular_size)
			para = Paragraph(val['pos'], style)
			w, h = para.wrap(text_width, text_height)
			next_line(h)
			next_line(h)
			para.drawOn(canvas, text_start, start)
			
			# the definition
			style = ParagraphStyle(name='definition', fontName='Lato-Regular', fontSize=regular_size)
			para = Paragraph(val['def'], style)
			w, h = para.wrap(text_width, text_height)
			next_line(h)
			para.drawOn(canvas, text_start, start)
			
			# synonyms
			if val['synonyms']:
				style = ParagraphStyle(name='synonyms', fontName='Lato-Regular', fontSize=regular_size)
				para = Paragraph(f"<strong>synonyms:</strong> {', '.join(val['synonyms'])}", style)
				w, h = para.wrap(text_width, text_height)
				next_line(h)
				para.drawOn(canvas, text_start, start)
			
			# antonyms
			if val['antonyms']:
				style = ParagraphStyle(name='antonyms', fontName='Lato-Regular', fontSize=regular_size)
				para = Paragraph(f"<strong>antonyms:</strong> {', '.join(val['antonyms'])}", style)
				w, h = para.wrap(text_width, text_height)
				next_line(h)
				para.drawOn(canvas, text_start, start)
			
			# notes
			if val['notes']:
				style = ParagraphStyle(name='notes', fontName='Lato-Regular', fontSize=regular_size)
				para = Paragraph(f"<strong>Notes:</strong> {val['notes']}", style)
				w, h = para.wrap(text_width, text_height)
				next_line(h)
				para.drawOn(canvas, text_start, start)
			
			# draw the image
			if val['image'] and not personal:
				img = load_image(os.path.join(str(val['path']), 'images', val['image']))
				img = cv2.resize(img, (img_dim, img_dim), interpolation=cv2.INTER_AREA)
	
		# draw image
		next_line(img_dim + 5)
		if not personal:
			img = cv2.imencode('.jpg', img)[1].tobytes()
			img = ImageReader(io.BytesIO(img))
			canvas.drawImage(img, inch / 2, height - img_dim - idx * height / 3 + inch / 8)
		
		# if time.time() - beg > 1:
		# 	break

	canvas.save()



if __name__ == '__main__':
	# load data
	data = get_data()
	
	# save json data to pdf
	data_to_pdf(data)