#runs Google Vision on a batch of images and prints their output to individual text files. 
#output .txts go in folder in the parent directory
#written by James Gisele, james.may.gisele@gmail.com

import base64
import os
import io
from google.cloud import vision
from google.cloud.vision import types
from googleapiclient.discovery import build
APIKEY = 'AIzaSyCcgY4MwelgM_TGBsyELyHxkDQ30GNnWAM'

def VisionTranscription(original_directory, final_directory):
	os.chdir(original_directory)
	if not os.path.isdir(final_directory):
		os.makedirs(final_directory)
	for i in os.listdir(original_directory):	#iterate through pngs in original directory
		filename = os.path.splitext(i)[0]
		if os.path.splitext(i)[1] != '.png':
			pass
		if filename[-5:] == "00000": #skipping the non text
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


og_directory = input("original directory?:")
folder_name = os.path.basename(og_directory) + "_txts"
fin_directory = os.path.dirname(og_directory) + "\%s" % folder_name
VisionTranscription(og_directory, fin_directory)

