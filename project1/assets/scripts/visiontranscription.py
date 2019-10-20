import base64 #provides functions to encode binary data to Base64 encoded format
import os #provides functions for interacting with the operating system
import io #provides core tools for working with streams
from google.cloud import vision #for integrating vision detection features within applications
from google.cloud.vision import types
from googleapiclient.discovery import build
APIKEY = 'AIzaSyCcgY4MwelgM_TGBsyELyHxkDQ30GNnWAM' #API key is a unique string that let's us access an API

""" This function runs Google Vision on a batch of images and prints their output to individual text files. output
text files go in folder in the specified parent directory. The function propmps the user for an original directory that contains
the images and it then runs Google Vision on them"""
def VisionTranscription(original_directory, final_directory):
	#change the current working directory to a specified path
	os.chdir(original_directory)
	#os.path.isdir checks whether the specified path is an existing directory or not
	#if not an existing directory create a directory
	if not os.path.isdir(final_directory):
		os.makedirs(final_directory)
	#os.listdir gets the list of all files and directories in the specified directory
	for i in os.listdir(original_directory):	#iterate through pngs in original directory
		#split the path into a pair root and ext.
		filename = os.path.splitext(i)[0]
		if os.path.splitext(i)[1] != '.png':
			pass
		if filename[-5:] == "00000": #skipping the non text
			pass
		else:
			print(i)
			textname=os.path.splitext(i)[0]
			#read binary
			image = open(i, 'rb')
			#perfom a feature detection on an image file by sending the contents of thr image file
			#as a base64 encoded string
			image_content = base64.b64encode(image.read())
			vservice = build('vision', 'v1', developerKey=APIKEY)
			language = 'eng'
			#run image detection and annotation for a batch of images
			#languageHints specifies the languagof text in the image
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
			responses = request.execute(num_retries=3) #
			output_text = responses['responses'][0]['textAnnotations'][0]['description']
			os.chdir(final_directory) #writing to file
			name_of_file = "%s.txt" % textname 
			#open the file for writing
			output_file = open(name_of_file,'w')
			try:
				output_file.write(output_text)
				output_file.close()
			except UnicodeEncodeError: 
				output_file.write("ERROR")
				output_file.close()
			os.chdir(original_directory)


og_directory = input("original directory?:") #prompt user for the original directory that contains images with readable texts
folder_name = os.path.basename(og_directory) + "_txts" #name the folder
fin_directory = os.path.dirname(og_directory) + "\%s" % folder_name
VisionTranscription(og_directory, fin_directory) #perform the transcription

