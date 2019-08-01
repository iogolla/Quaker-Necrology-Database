#converting from j2k to png
#using Wand binding for Image Magick to run automated script with prompting for initial directory
#and then using Google Vision API to extract text to a text document
#pictures go in one folder, text goes in another in the same directory
import os
import sys, getopt
import base64
import io
from wand.image import Image 
from google.cloud import vision
from google.cloud.vision import types
from googleapiclient.discovery import build
from os.path import dirname, abspath
APIKEY = 'AIzaSyCcgY4MwelgM_TGBsyELyHxkDQ30GNnWAM'

		
#converting to png, saving to a subdirectory of the same name as original directory			
def batchConvert(original_directory, final_directory):
	os.chdir(original_directory)
	if not os.path.isdir(final_directory):
		os.makedirs(final_directory)
	for i in os.listdir(original_directory): #iterate through j2ks in original directory
		if os.path.splitext(i)[1] == '.j2k':
			filename = os.path.splitext(i)[0]
			if filename[-4:] == "0000": #skipping the first one which doesn't contain any info
				pass
			print(i)
			try:
				with Image(filename=i, resolution=300) as original:
					with original.convert('png') as converted:
						# operations to a png image...
						converted.format = 'png'
						converted.type = 'grayscale' 
						converted.transform(resize='%50')
						os.chdir(final_directory)
						converted.save(filename='%s.png' % filename)					
						os.chdir(original_directory)
			except:
				print("There was an error with %s" % i)
				os.chdir(final_directory)
				name_of_file = "%s.txt" % os.path.splitext(i)[0]
				error_file = open(name_of_file,'w')
				error_file.write("There was an error with %s" % i)
				error_file.close()
				os.chdir(original_directory)
		else:
			pass	
					

og_j2k_directory = input("original directory?:")
folder_name = os.path.basename(og_j2k_directory) + "_pngs"
fin_png_directory = os.path.dirname(og_j2k_directory) + "\%s" % folder_name
batchConvert(og_j2k_directory, fin_png_directory)


def VisionTranscription(original_directory, final_directory):
	os.chdir(original_directory)
	if not os.path.isdir(final_directory):
		os.makedirs(final_directory)
	for i in os.listdir(original_directory): #iterate through pngs in original directory
		if os.path.splitext(i)[1] != '.png':
			pass
		else:
			print(i)
			textname=os.path.splitext(i)[0]
			image = open(i, 'rb')
			image_content = base64.b64encode(image.read())
			vservice = build('vision', 'v1', developerKey=APIKEY)
			language = 'eng'
			request = vservice.images().annotate(body={
					'requests': [{
								'image': {
											'content': image_content.decode('UTF-8')
											},
								'imageContext': {
											'languageHints': [language]},
											'features': [{
								'type': 'TEXT_DETECTION'
												}]
											}]
							})
			responses = request.execute(num_retries=3)
			output_text = responses['responses'][0]['textAnnotations'][0]['description']
			os.chdir(final_directory) #writing to file
			name_of_file = "%s.txt" % textname 
			output_file = open(name_of_file,'w')
			try:
				output_file.write(output_text)
				output_file.close()
			except UnicodeEncodeError: 
				output_file.write("ERROR")
				output_file.close()
			os.chdir(original_directory)
			
og_directory = fin_png_directory
folder_name = os.path.basename(og_directory) + "_txts"
fin_text_directory = os.path.dirname(og_directory) + "\%s" % folder_name
VisionTranscription(og_directory, fin_text_directory)
