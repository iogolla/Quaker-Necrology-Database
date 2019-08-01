#parses text files from google vision to extract the citation information into one csv file. 
#if there are errors during this process, prints to both command and the csv file.
#written by James Gisele, james.may.gisele@gmail.com

#batchParse is the main function, calls all the other functions here after getting the input of
#what the folder containing the files is.

import os
import sys, getopt
import base64
import io
import csv
from os.path import dirname, abspath


def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)
	
def hasAlpha(inputString):
	return any(char.isalpha() for char in inputString) 

def removePunct(inputString, isBirthDeath): #removes end commas and dashes, and parentheses from non-volume items. called by both batchParse and firstMiddleLastParser
	n = 0
	while n <= 5 and len(inputString) > 1: #iterates several times just in case there's a comma then a space then a comma, etc.
		n += 1
		#cases of punctuation you don't want as first/last character, but DO want some places:
		if inputString[-1] == " ":
			inputString = inputString[:-1]
		if inputString[0] == " ": 
			inputString = inputString[1:]
		if inputString[-1] == ",": 
			inputString = inputString[:-1]
		if inputString[0] == ",": 
			inputString = inputString[1:]
		if inputString[-1] == "-": 
			inputString = inputString[:-1]
		if inputString[-1] == "(":
			inputString = inputString[:-1]
		#case(s) of common punctuation Google Vision gives you that you don't want anywhere:
		if "»" in inputString:
			inputString = inputString.replace("»", "")
		# there are some characters you don't want in birth or death entries but might want elsewhere
		if isBirthDeath == True:
			for char in inputString:
				if char == ")":
					inputString = inputString.replace(")", "")
				if char == "(":
					inputString = inputString.replace("(", "")
				if char == ".":
					inputString = inputString.replace(".", "")
			if inputString[0].isalpha():
				inputString = inputString[1:]
			if inputString[-1].isalpha():
				inputString = inputString[:-1]
	if "riend" in inputString and "Friend" not in inputString and "friend" not in inputString:	#if there's a "riend" in the string,,, it's definitely friend*
		inputString = inputString.replace("riend", "Friend")
	return inputString
	
	
def firstMiddleLastParser(inputString):  #parses the first name and middle name, last name, any secondary last names, and any suffixes. called by namesAndBirthDeathParser
	input_commas = inputString.split(",")
	input_space = inputString.split(" ")
	lastname = input_commas[0]
	firstname_middlename = inputString #usually gets overwritten
	firstname = middlename = suffix = second_last_name = ""			
	is_suffix = False
	if len(input_commas) > 1: #if there are commas
		firstname_middlename = input_commas[1] #the first and middle if only 1 comma and no numbers--- gets overwritten if more than 1 comma
	if len(input_commas) <= 1: #if no commas in the line, parse by spaces
		if len(input_space) == 2:
			firstname_middlename, lastname = inputString.split(" ")
		if len(input_space) == 3:
			firstname_middlename = input_space[0] + " " + input_space[1]
			lastname = input_space[1]
		if len(input_space) == 4:
			firstname_middlename = input_space[0] + " " + input_space[1]
			lastname = input_space[2] + " " + input_space[3]
	if len(input_commas) == 2 and inputString[-1] == ",": #then parse by spaces as well, but diff order
		if len(input_space) == 2:
			lastname, firstname_middlename = inputString.split(" ")
		if len(input_space) == 3:
			firstname_middlename = input_space[1] + " " + input_space[2]
			lastname = input_space[0]
	if len(input_commas) == 4: #if there are three commas, then check for suffix
		second_comma = input_commas[1]
		third_comma = input_commas[2]
		if "jr" in second_comma or "Jr" in second_comma or "sr" in second_comma or "Sr" in second_comma:
			suffix = second_comma
			is_suffix = True
			if not is_suffix: #then it's another last name
				second_last_name += second_comma
			firstname_middlename = input_commas[2]
		elif "jr" in third_comma or "Jr" in third_comma or "sr" in third_comma or "Sr" in third_comma:
			suffix += third_comma
			is_suffix = True
			if not is_suffix: #then it's another last name
				second_last_name += third_comma
			firstname_middlename = input_commas[1]
	if "(" in firstname_middlename and ")" in firstname_middlename: #then there's an old last name in parenthesis rather than separated by commas
		first = inputString.index("(")
		last = inputString.index(")") + 1
		second_last_name = inputString[first:last]
		firstname_middlename = firstname_middlename.replace(second_last_name, "")
		second_last_name = second_last_name[1:-1] 
	firstname_middlename = removePunct(firstname_middlename, False)
	firstname = firstname_middlename
	if " " in firstname_middlename: #parsing out the middle name from the first name if possible; if not, just leaves as part of firstname
		try:
			firstname, middlename = firstname_middlename.split(" ")
		except ValueError:
			pass
	if "." in firstname_middlename: #sometimes it's a period separating first & middle instead
		try:
			firstname, middlename = firstname_middlename.split(".")
		except ValueError:
			pass
	return firstname, middlename, lastname, second_last_name, suffix


def namesAndBirthDeathParser(inputString, og_first, og_middle, og_lastname, og_birth, og_death, filename): #parses the line containing the name and birth/death date.
	#takes the original first/middle/last/etc so that if inputString doesn't contain them it can just pass them right through unchanged, rather than overwriting
	hasDatesAndName = False
	only_name_on_first_line = True
	only_dates_on_first_line = True
	#these variables get overwritten if the inputstring contains this info, and stay if inputstring does not
	firstname = og_first
	middlename = og_middle
	lastname = og_lastname
	birth = og_birth
	death = og_death
	suffix = second_last_name = ""
	if len(inputString) <= 1:
		return firstname, middlename, lastname, second_last_name, suffix, birth, death, hasDatesAndName, only_name_on_first_line, only_dates_on_first_line
	if len(inputString) >= 4: #making sure it's not some random badly Google Vision'd letters as some entries have 
		for char in inputString: 
				if inputString[0].isalpha() or inputString[1].isalpha(): #if there's a name in inputString
					only_dates_on_first_line = False
					if char.isnumeric(): #if there is also a number in input string, you can parse name vs date by that
						hasDatesAndName = True
						only_name_on_first_line = False
						index = inputString.index(char) #index of first number
						split = index - 1 #index of whatever comes before first number
						names = inputString[:index]
						birthdeath = inputString[split:]
						#handling firstname middlename and lastname
						firstname, middlename, lastname, second_last_name, suffix = firstMiddleLastParser(names)
						#handling birth and death
						if birthdeath[0] == "-" or birthdeath[1] == "-": #no birth
							birth = ""
							death = birthdeath
						if birthdeath[0] == " ":
							birthdeath = birthdeath[1:]
						if birthdeath[-1] == " ":
							birthdeath = birthdeath[:-1]
						if birthdeath[-1] == ".":
							birthdeath = birthdeath[:-1]
						if len(birthdeath.split("-")) == 2:
							birth, death = birthdeath.split("-")
						elif " " in birthdeath:
							if "-" not in birthdeath:
								if len(birthdeath.split(" ")) == 2:
									birth, death = birthdeath.split(" ")
						else:
							birth = ""
							death = birthdeath
						break
		if hasDatesAndName == False and only_dates_on_first_line == False: # if there's no dates, it's just the name
			only_name_on_first_line = True
			firstname, middlename, lastname, second_last_name, suffix = firstMiddleLastParser(inputString)
		elif hasDatesAndName == False and only_dates_on_first_line == True: #if there's no name in inputstring, it's just the date
			birthdeath = inputString
			if len(birthdeath) > 1:
				if birthdeath[0] == "-" or birthdeath[1] == "-": #no birth
					birth = " "
					death = birthdeath
				elif len(birthdeath.split("-")) > 1:
					birth, death = birthdeath.split("-")
				else:
					death = birthdeath
					birth =  " "
	return firstname, middlename, lastname, second_last_name, suffix, birth, death, hasDatesAndName, only_name_on_first_line, only_dates_on_first_line
		
def pubMonthYearParser(volume): #used in pub parser below to parse volume info into month and year
	month = year = ""
	if "(" in volume and ")" in volume: #then there's a year associated with the publication
		first = volume.index("(")
		last = volume.index(")") + 1
		year = volume[first:last]
		volume = volume.replace(year, "")
		year = year[1:-1] 
	if hasAlpha(year): #parsing the publication month, if there is one
		for char in year:
			if char.isnumeric():
				index = year.index(char) #index of first number
				split = index - 1 #index of whatever comes before first number
				month = year[:split]
				year = year[index:]	
				break
	if "," in year: #add the day to the month 
		month = month + " " + year.split(",")[0]
		year = year.replace(year.split(",")[0], "")
	return month, year, volume
	
def publicationParser(inputString, og_publication_name, volOnly): #parses the line containing publication and/or volume info
	vol_in_this_line = False
	publication_name = volume = month = year = page = volume_dump = " "
	if len(inputString) <= 1:
		return publication_name, volume, month, year, page, volume_dump, vol_in_this_line
	for char in inputString:
		if char.isnumeric():
			index = inputString.index(char) #index of first number
			split = index - 1 #index of whatever comes before first number
			publication_name = inputString[:split]
			volume_info = inputString[index:]
			vol_in_this_line = True
			break
		elif char == "(":
			index = inputString.index(char)
			split = index - 1 #index of whatever comes before first number
			publication_name = inputString[:split]
			volume_info = inputString[index:]
			vol_in_this_line = True
			break
		else: #no numbers or parentheses in line
			vol_in_this_line = False
			continue
	if vol_in_this_line == False: # if there are no numbers ( ie vol info) in line
		publication_name = inputString
	else: #if there are numbers (ie vol info) in line
		if volOnly == True:
			publication_name = og_publication_name #then publication name shouldn't be changed
		if ":" in volume_info:
			volume_dump = " "
			try:
				volume, page = volume_info.split(":")
				month, year, volume = pubMonthYearParser(volume)
			except ValueError:
				volume_dump = volume_info
		elif ")" in volume_info: 
			index = volume_info.index(")") + 1
			volume = volume_info[:index]
			page = volume_info[index:]
			month, year, volume = pubMonthYearParser(volume)
		else:
			volume_dump = volume_info
	if len(page) > 0:
		if page[0] == ":":
			page = page[1:]
	return publication_name, volume, month, year, page, volume_dump, vol_in_this_line	


def batchParse(original_directory, final_directory): #main function
	output_file_name = "%s.csv" % os.path.basename(og_text_directory)[:-5]
	if not os.path.isdir(final_directory):
		os.makedirs(final_directory)
	#writing the headers to the file
	os.chdir(final_directory)
	with open(output_file_name, 'a', newline='') as csv_output:
		header_row = ["lastname", "first name", "middle name", "second last name", "suffix", "birth", "death", "publication name", "volume", "publication month (and day)", "publication year", "page", "volume (unable to sort)", "second publication" , "second volume" , "second publication year", "second page", "second volume (unable to sort)"]
		writer = csv.writer(csv_output)
		writer.writerow(header_row)
		csv_output.close()
	#extracting and parsing .txts
	os.chdir(original_directory)
	directory = os.listdir(original_directory)
	for file in directory: #iterate through .txts in original directory
		lastname = firstname = middlename = second_last_name = suffix = birth = death = publication_name = volume = month = year = page = volume_dump = second_publication = second_volume = second_month = second_year = second_page = second_volume_dump = " "	#setting empty strings so if there's no value for an element it ends up blank
		if os.path.splitext(file)[1] != '.txt':
			pass
		else:
			os.chdir(original_directory)
			#opening file
			with open(file, 'r') as file_to_read:
				file_text = file_to_read.read()
				split_by_line = file_text.split("\n")
				file_to_read.close()
			filename = file
			#parsing text
			if split_by_line[0] == "ERROR":
				print('%s is an error file and was not appended to the csv' % filename)
				pass
			else:
				#first line
				if len(split_by_line) >= 1: # if there are one or more lines
					if len(split_by_line[0]) <= 4 and len(split_by_line) > 1 and split_by_line[0][0].isalpha(): #then it's probably just a Vision transcription error and the second line should be appended to the first
						split_by_line[0] += split_by_line[1]
						split_by_line[1] = "" 
						firstname, middlename, lastname, second_last_name, suffix, birth, death, hasDatesAndName, only_name_on_first_line, only_dates_on_first_line = namesAndBirthDeathParser(split_by_line[0], split_by_line[0], "", lastname, birth, death, filename)
					else: #the usual case
						firstname, middlename, lastname, second_last_name, suffix, birth, death, hasDatesAndName, only_name_on_first_line, only_dates_on_first_line = namesAndBirthDeathParser(split_by_line[0], split_by_line[0], "", lastname, birth, death, filename)
				#second line and third line
				if len(split_by_line[1]) == 0: #this is the case where the second line is empty and has been appended to the first. so just check the third line on
					if len(split_by_line) >= 3: #if there's a third line
						publication_name, volume, month, year, page, volume_dump, vol_in_this_line = publicationParser(split_by_line[2], split_by_line[2], False)
						if len(split_by_line) >= 4: #if there's a fourth line 
							if vol_in_this_line == False: #if there wasn't volume info in the third line, check if there's a fourth line that contains volume info
								publication_name, volume, month, year, page, volume_dump, vol_in_this_line = publicationParser(split_by_line[3], publication_name, True)
							if vol_in_this_line == True: #but if there's vol info in the third line and ALSO a fourth line, this is just a second set of publication info
								second_publication, second_volume, second_month, second_year, second_page, second_volume_dump, vol_in_this_line = publicationParser(split_by_line[3], split_by_line[3], False)
								if vol_in_this_line == False: #and make sure to check the fifth line for second volume info.
									if len(split_by_line) >= 5:
										second_publication, second_volume, second_month, second_year, second_page, second_volume_dump, vol_in_this_line = publicationParser(split_by_line[4], second_publication, True)
				elif hasDatesAndName == True:	#the first line had names + dates both. so run pub parser on second + third line
					if len(split_by_line) >= 2: #if there's a second line
						publication_name, volume, month, year, page, volume_dump, vol_in_this_line = publicationParser(split_by_line[1], split_by_line[1], False) #then run publication parser on second line
						if len(split_by_line) >= 3: 
							if vol_in_this_line == False: #if there wasn't volume info in the second line, check if there's a third line that contains volume info
								publication_name, volume, month, year, page, volume_dump, vol_in_this_line = publicationParser(split_by_line[2], publication_name, True)
							if vol_in_this_line == True: #but if there's vol info in the second line and ALSO a third line, this is just a second set of publication info
								second_publication, second_volume, second_month, second_year, second_page, second_volume_dump, vol_in_this_line = publicationParser(split_by_line[2], split_by_line[2], False)
								if vol_in_this_line == False: #and make sure to check the fourth line for second volume info.
									if len(split_by_line) >= 4:
										second_publication, second_volume, second_month, second_year, second_page, second_volume_dump, vol_in_this_line = publicationParser(split_by_line[3], second_publication, True)
				elif only_dates_on_first_line == True: #then the name info is on the second line
					if len(split_by_line) >= 2: #so if there's a second line, check it for the name
						firstname, middlename, lastname, second_last_name, suffix, birth, death, hasDatesAndName, only_name_on_first_line, only_dates_on_first_line = namesAndBirthDeathParser(split_by_line[1], firstname, middlename, lastname, birth, death, filename)
						if len(split_by_line) >= 3: #and check the third for publication info	
							publication_name, volume, month, year, page, volume_dump, vol_in_this_line = publicationParser(split_by_line[2], publication_name, False)
							if vol_in_this_line == False: #if there wasn't volume info in the third line
								if len(split_by_line) >= 4: #check the fourth for volume info
									publication_name, volume, month, year, page, volume_dump, vol_in_this_line = publicationParser(split_by_line[3], publication_name, True)
									if len(split_by_line) >= 5: #if there's a fifth line
										second_publication, second_volume, second_month, second_year, second_page, second_volume_dump, vol_in_this_line = publicationParser(split_by_line[4], split_by_line[4], False)
										if vol_in_this_line == False: #and make sure to check the sixth line for second volume info.
											if len(split_by_line) >= 6:
												second_publication, second_volume, second_month, second_year, second_page, second_volume_dump, vol_in_this_line = publicationParser(split_by_line[5], second_publication, True)				
				elif only_name_on_first_line == True: #then check the second line for birth, death if it's short and publication if it's not
					if len(split_by_line) >= 2: #if there's a second line 
						if len(split_by_line[1]) < 10:#and it's short, check it for birth and death (trash is an unused variable so that only the birth/death get overwritten)
							trash, trash, trash, trash, trash, birth, death, hasDatesAndName, only_name_on_first_line, only_dates_on_first_line = namesAndBirthDeathParser(split_by_line[1], firstname, middlename, lastname, birth, death, filename)
							if len(split_by_line) >= 3: #and check the third for publication info	
								publication_name, volume, month, year, page, volume_dump, vol_in_this_line = publicationParser(split_by_line[2], publication_name, False) 
								if vol_in_this_line == False: #if there wasn't volume info in the third line
									if len(split_by_line) >= 4: #check the fourth for volume info									
										publication_name, volume, month, year, page, volume_dump, vol_in_this_line = publicationParser(split_by_line[3], publication_name, True)				
										if len(split_by_line) >= 5: #if there's a fifth line
											second_publication, second_volume, second_month, second_year, second_page, second_volume_dump, vol_in_this_line = publicationParser(split_by_line[4], split_by_line[4], False)
											if vol_in_this_line == False: #and make sure to check the sixth line for second volume info.
												if len(split_by_line) >= 6:
													second_publication, second_volume, second_month, second_year, second_page, second_volume_dump, vol_in_this_line = publicationParser(split_by_line[5], second_publication, True)									
						else: #check second line for publication info 
							publication_name, volume, month, year, page, volume_dump, vol_in_this_line = publicationParser(split_by_line[1], split_by_line[1], False) #then run publication parser on second line
							if vol_in_this_line == False: #if there wasn't volume info in the second line, check if there's a third line that contains volume info
								if len(split_by_line) >= 3:
									publication_name, volume, month, year, page, volume_dump, vol_in_this_line = publicationParser(split_by_line[2], publication_name, True)
									if len(split_by_line) >= 4: #if there's a fourth line
										second_publication, second_volume, second_month, second_year, second_page, second_volume_dump, vol_in_this_line = publicationParser(split_by_line[3], split_by_line[3], False)
										if vol_in_this_line == False: #and make sure to check the fifth line for second volume info.
											if len(split_by_line) >= 6:
												second_publication, second_volume, second_month, second_year, second_page, second_volume_dump, vol_in_this_line = publicationParser(split_by_line[4], second_publication, True)			
				else: #error	
					print("error: " + output_file_name)
				#removing any commas etc, clean up punctuation
				firstname = removePunct(firstname, False)
				middlename = removePunct(middlename, False)
				volume = removePunct(volume, False)
				year = removePunct(year, False)
				month = removePunct(month, False)
				birth = removePunct(birth, True)
				death = removePunct(death, True)
				publication_name = removePunct(publication_name, False)
				second_volume = removePunct(second_volume, False)
				second_year = removePunct(second_year, False)
				second_publication = removePunct(second_publication, False)
				second_month = removePunct(second_publication, False)
				#writing to file	
				os.chdir(final_directory)
				with open(output_file_name, 'a', newline='') as csv_output:
					if lastname == "CED" or lastname == "R G B" or lastname == "B" or publication_name == "Card and filing": #checking for non-citation images
						pass
					else:
						new_row = [lastname, firstname, middlename, second_last_name, suffix, birth, death, publication_name, volume, month, year, page, volume_dump, second_publication, second_volume, second_month, second_year, second_page, second_volume_dump]
						writer = csv.writer(csv_output)
						writer.writerow(new_row)
						csv_output.close()
				
				
				
				
og_text_directory = input("directory of .txts?:")
if og_text_directory.endswith('\\'):
	og_text_directory = og_text_directory[:-1]
folder_name = os.path.basename(og_text_directory)[:-5] + "_csv"
fin_directory = os.path.dirname(og_text_directory) + "\%s" % folder_name
batchParse(og_text_directory, fin_directory)







