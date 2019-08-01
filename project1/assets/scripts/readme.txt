QUESTIONS: James Gisele '19, james.may.gisele@gmail.com


HOW THIS WORKS:
-take .j2ks and run them through pillow or wand script to get them as smaller 
.pngs (j2ktopng.py scripts)
-take these .pngs and run them through Google Vision script to get a set of .txts with their 
content transcribed (vision_transcription.py)
-take these .txts and run them through the parsing script to get a .csv of their contents parsed into first name, 
publication name, etc (parsing.py)
-(eventually) build a website to host all of these on (I haven't gotten that far yet)


SCRIPTS AND TEXT FILES IN THIS FOLDER:
-requirements.txt: this is just a pip freeze output of the Python environment I was using for this project.

-converted_list: holds the names of drives I've checked for images and how many folders and which 
were in each drive. If a drive is not on this list, I haven't touched the files on it.

-j2ktopng_pillow.py: converts a folder of j2ks (JPEG-2000) to pngs and dumps them in a folder named after 
the first but with _pngs appended, in the parent directory of the j2k folder. uses pillow.

-j2ktopng_wand.py: converts a folder of j2ks to pngs and dumps them in a folder named after 
the first but with _pngs appended, in the parent directory of the j2k folder. uses wand binding for 
imagemagick. you need wand 0.5.0; as of time of writing, 0.5.1 seemed to be broken & not working 
correctly. Only use if pillow isn't working for you, because ImageMagick was really finnicky especially 
on Ubuntu.

-visiontranscription.py: batch-transcribes a folder of .pngs and directs the output to a _txts folder 
in the parent directory. transcibes by sending a request to the google vision API for each image. IMAGE FILE 
SIZES MUST BE SMALL or google vision can't convert!

-convert_and_vision_pillow.py: compiles both the above scripts (j2ktopng and visiontranscription) into one,
using pillow.
-convert_and_vision_wand.py: compiles both the above scripts into one, using imagemagick and wand.

-parsing.py: takes a folder of .txts and parses them into .csv format with headers for first name, 
last name, publication, death date, etc. if a csv of the same name/location already exists, just appends new 
entries to this original file. outputs to a _csv folder in the parent directory.



OTHER FILES/FOLDERS:
-All_Files folder (in separate zip): contains all the .pngs. and .txts I've been working with. Named as they were in
the drives they came from. I didn't include the .j2ks because they're on the drives and they were too big to reasonably zip
and upload.
-Testing folder (in separate zip): contains two folders and csvs--- one full of a bunch of files all copied from the All_Files
folder (big_test) and one full of a smaller set of .txt files that are currently not parsing well (small_test) and their
corresponding csvs. I've been slowly making my way through the big_test files and pulling ones that aren't parsing well
to small_test, and then running just small_test through the parsing script and making changes to the script to get a better parser.
the current parser works on about 94-98% of the images, so this is fine-tuning for the most part.


KNOWN ISSUES:
-Google Vision is good but not perfect. The parsing script does its best to catch some of the common errors
manually and clean up the text before sending to .csv, but there isn't perfect accuracy in the png-to-text. 
Usually this manifests in new lines where there should be none and incorrect characters, but on some images
there image is so blurry from poor scanning that Vision can't parse it at all. In these situations, the .txt 
script just prints "ERROR" to the .txt file for that image. This is then picked up by the parser so that the file is skipped. 
So if you change the Vision error message that prints to file, go back and change the handler in the parser as well 
(or it'll get messed up by the new error message).
-the first 1-3 images on each roll are not citations and thus throw errors for both Vision and the parser. I've handled these
within the parser and vision by just hard coding in handlers for strings which indicate that it's not a citation,
but you should probably find a more reliable way to do this especially in the parser. . . .
-Parser errors--- there are still problems parsing some entries! The citation style on all the images is Super inconsistent,
so once you have all the images Vision'd it's probably worth just going through and making sure there wasn't one folder
with drastically different citation style or something equally frustrating.
-ImageMagick does not work on Andy's Ubuntu machine for .j2k conversion. Use Pillow in general probably, 
but especially on that machine.


STUFF TO DO:
-All the files for this project are on drives in .j2k format. At some point they'll all need to be both 
converted to .png and ran through Vision. The files in the All_Files folder are a smaller sample I used to write the 
scripts. Note: Pillow takes a few seconds for each image, and ImageMagick a few minutes, even on good processors. 
Vision similarly takes a few moments to transcribe every file. And there are ~70,000? files if I remember correctly. 
So this will take time, and need lots of drive space!
-Check the small_test folder in the Testing folder, it contains .txts that aren't parsing properly that I've found
from the test files I've been using. The parser can hopefully be edited to parse these correctly with a few more lines,
these are just ones I hadn't gotten to yet.
-Every time I run the parser on a new batch of images, there's a few with a new Google Vision-based error, 
citation style, etc. Andy mentioned Spacy might be helpful--- I didn't know about Spacy when I wrote the parser 
so I've been building on what I've done, but worth checking out to see if that is helpful in the remaining cases.
-Obviously, build a site to host all of this. I think Mike was originally looking for this to be a Django project.
