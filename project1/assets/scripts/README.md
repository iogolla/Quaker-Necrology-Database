# Quaker Necrology Database
[Link to the project's website](http://134.209.121.250)

## Scripts and Text Files

* **j2ktopng_pillow.py** this is a python function that converts a folder of `j2ks` (JPEG-2000) to `pngs` and dumps them in a folder named after the first but with `pngs` appended, in the parent directory of the `j2k` folder.

* **j2ktopng_wand.py** : this converts a folder of `j2ks` to pngs and dumps them in a folder named after 
the first but with `pngs` appended, in the parent directory of the `j2k` folder. Uses wand binding for 
imagemagick. you need wand 0.5.0; as of time of writing, 0.5.1 seemed to be broken & not working 
correctly. Only use if pillow isn't working for you, because ImageMagick was really finnicky especially 
on Ubuntu.

* **visiontranscription.py**: this batch-transcribes a folder of `pngs` and directs the output to a `txts` folder in the parent directory. Transcibes by sending a request to the google vision API for each image. **IMAGE FILE SIZES MUST BE SMALL** or google vision can't convert!

* **convert_and_vision_pillow.py**: this compiles both the above scripts (j2ktopng and visiontranscription) into one, using pillow.

* **convert_and_vision_wand.py**: compiles both the above scripts into one, using imagemagick and wand.

* **parsing.py**: takes a folder of `txts` and parses them into `csv` format with headers for first name, 
last name, publication, death date, etc. if a csv of the same name/location already exists, just appends new 
entries to this original file. outputs to a csv folder in the parent directory.

## How this works
* take .j2ks and run them through pillow or wand script to get them as smaller 
.pngs (j2ktopng.py scripts)
* take these .pngs and run them through Google Vision script to get a set of .txts with their 
content transcribed (vision_transcription.py)
* take these .txts and run them through the parsing script to get a .csv of their contents parsed into first name, 
publication name, etc (parsing.py)

More information can be found in the in-code documentation.


