#!/usr/bin/env python3
import requests
from PIL import Image
from resizeimage import resizeimage



def resize_remote(url: str) -> Image:
	# Takes in an image URL as an argument
	# Returns a resized PIL Image object with instagram compatible aspect ratio.
	# Or None if unsuccessful. 

	MIN_ASPECT_RATIO = 0.9
	MAX_ASPECT_RATIO = 1.8


	# Retrieve the image from URL.
	try:
		img = Image.open(requests.get(url, stream=True).raw)
	except Exception as e: 
		print(e)
		return None	
			
	# Detect the size and find the new dimension for the image. 
	width, height = img.size
	aspect_ratio = width/height

	if (aspect_ratio >= MIN_ASPECT_RATIO) and (aspect_ratio <= MAX_ASPECT_RATIO):
		return img

	elif aspect_ratio < MIN_ASPECT_RATIO:
		new_height = height
		new_width = MIN_ASPECT_RATIO*new_height

	elif aspect_ratio > MAX_ASPECT_RATIO:
		new_width = width
		new_height = new_width/MAX_ASPECT_RATIO

	else:
		print("INVALID ASPECT RATIO")
		return None

	# Resize the image to instagram supported size. 
	try: 
		img = resizeimage.resize_contain(img, [int(new_width), int(new_height)])
		return img
	except Exception as e:
		print(e)
		return None



def resize_image(image: Image) -> Image:
	# Takes in a PIL Image object
	# Returns a resized PIL Image object with instagram compatible aspect ratio.
	# Or None if unsuccessful. 

	MIN_ASPECT_RATIO = 0.9
	MAX_ASPECT_RATIO = 1.8

			
	# Detect the size and find the new dimension for the image. 
	width, height = image.size
	aspect_ratio = width/height

	if (aspect_ratio >= MIN_ASPECT_RATIO) and (aspect_ratio <= MAX_ASPECT_RATIO):
		return image

	elif aspect_ratio < MIN_ASPECT_RATIO:
		new_height = height
		new_width = MIN_ASPECT_RATIO*new_height

	elif aspect_ratio > MAX_ASPECT_RATIO:
		new_width = width
		new_height = new_width/MAX_ASPECT_RATIO

	else:
		print("INVALID ASPECT RATIO")
		return None

	# Resize the image to instagram supported size. 
	try: 
		image = resizeimage.resize_contain(image, [int(new_width), int(new_height)])
		return image
	except Exception as e:
		print(e)
		return None