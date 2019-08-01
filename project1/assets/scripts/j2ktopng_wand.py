#converting from j2k to png
#using Wand binding for Image Magick to run automated script with prompting for initial directory
import os
import sys, getopt
from wand.image import Image 


		
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
			

og_directory = input("original directory?:")
folder_name = os.path.basename(og_directory) + "_pngs"
fin_directory = os.path.dirname(og_directory) + "\%s" % folder_name
batchConvert(og_directory, fin_directory)

