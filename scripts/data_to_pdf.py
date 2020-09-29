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



def data_to_pdf(data: dict) -> None:
	# register required fonts
	pdfmetrics.registerFont(TTFont('Lato-Regular', 'Lato-Regular.ttf'))
	pdfmetrics.registerFont(TTFont('Lato-Bold', 'Lato-Bold.ttf'))
	pdfmetrics.registerFont(TTFont('Lato-Italic', 'Lato-Italic.ttf'))
	pdfmetrics.registerFont(TTFont('Lato-SemiBold', 'Lato-SemiBold.ttf'))
	
	# initialization
	width, height = 8.5 * inch, 11 * inch
	idx, mod = -1, 3
	img_dim = 200
	text_width, text_height = width - img_dim - 150, height // 3
	text_start = img_dim + inch / 1.5
	start, center = height, width / 2
	line_offset, word_offset = 14, 20
	heading_size, regular_size = 24, 12
	
	# create an empty canvas
	canvas = Canvas('GREPrep.pdf')
	
	# write the header
	# canvas.setFont('Lato-Regular', heading_size)
	# canvas.drawCentredString(center, start, 'GREPrep')
	# canvas.showPage()
	
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
		para.wrap(text_width, text_height)
		para.drawOn(canvas, text_start, start)
		
		for val in value:
			# the part of speech
			next_line(line_offset)
			style = ParagraphStyle(name='pos', fontName='Lato-Italic', fontSize=regular_size)
			para = Paragraph(val['pos'], style)
			para.wrap(text_width, text_height)
			para.drawOn(canvas, text_start, start)
			
			# the definition
			style = ParagraphStyle(name='definition', fontName='Lato-Regular', fontSize=regular_size)
			para = Paragraph(val['def'], style)
			w, h = para.wrap(text_width, text_height)
			next_line(h)
			para.drawOn(canvas, text_start, start)
			
			# notes
			if val['notes']:
				next_line(line_offset)
				style = ParagraphStyle(name='notes', fontName='Lato-SemiBold', fontSize=regular_size)
				para = Paragraph('notes:', style)
				para.wrap(text_width, text_height)
				para.drawOn(canvas, text_start, start)
				
				style = ParagraphStyle(name='notes', fontName='Lato-Regular', fontSize=regular_size)
				para = Paragraph(val['notes'], style)
				w, h = para.wrap(text_width, text_height)
				next_line(h)
				para.drawOn(canvas, text_start, start)
			
			if val['image']:
				img = load_image(os.path.join(str(val['path']), 'images', val['image']))
				img = cv2.resize(img, (img_dim, img_dim), interpolation=cv2.INTER_AREA)
	
		# draw image
		next_line(img_dim + 5)
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