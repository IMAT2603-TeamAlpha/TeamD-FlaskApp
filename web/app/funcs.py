from flask import current_app
import os, binascii
from PIL import Image 

# save image file name
def save_picture(form_picture):
    	# generate a random hex string
	random_hex = binascii.b2a_hex(os.urandom(8))
	# split filename and extension
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = str(random_hex) + str(f_ext)
	picture_path = os.path.join(current_app.root_path, 'static/car_pics', picture_fn)
	# resize image
	output_size = (300, 400)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	# return image file 
	return picture_fn

#Format numbers (i.e. 1234567 -> 1,234,567)
def numberFormat(value):
	return format(int(value), ',d')