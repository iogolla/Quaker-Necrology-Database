
# Quaker Necrology Database
[Link to the project's website]()

## Introduction

Quaker Necrology is a datatbase that collects and displayes the index of death notices and obituaries from Quaker periodicals from 1828 to the present. The database serves as an index and not a complete abstract of the information found in each obituary. It includes the information that we thought was necessary for the purposes of identification. That information includes the fullnames, dates of birth and death, the Quaker periodicals, and the years and volumes of publication. Below are the titles of the periodicals:

* The American Friend 1894-1960 (Five Years Meeting – Orthodox)
* Evangelical Friend 1905-1914, 1929-1994 (Ohio)
* Friend Bulletin 1934-2008 (Pacific Yearly Meeting)
* Friends Weekly Intelligencer 1844-1853 (Philadelphia, Pa.- Hicksite)
* Friends Intelligencer 1853-1885 (Philadelphia, Pa.)
* Friends Intelligencer and Journal 1888-1901 (Philadelphia, Pa.)
* Friends Intelligencer 1902-1955 (Philadelphia, Pa.)
* Friends Review 1848-1894 (Philadelphia, Pa.)
* Friends Journal 1955-2012 (Philadelphia, Pa.)
* Quaker Life 1960-2012 (Friends United Meeting, Indiana)

The record reference detailed above were obtained from a set of cards from the Special Collections at Haverford College Libraries. Each index card typically includes: name of the deceased, birth and death years (where available), and the title of the periodical the death notice appeared in, including page number.

A sample card is shown below: 




Quaker Necrology Database also allows users to send suggestions or comments on matters related to the Quakers enlisted. We welcome anyone with any additional information/suggestions to contact us.

## Project Components
### Scripts and Text Files in [this]() folder:

* **j2ktopng_pillow.py** this is a python function that converts a folder of **j2ks** (JPEG-2000) to **pngs** and dumps them in a folder named after the first but with **pngs** appended, in the parent directory of the **j2k** folder.

* **j2ktopng_wand.py** : this converts a folder of **j2ks** to pngs and dumps them in a folder named after 
the first but with **pngs** appended, in the parent directory of the **j2k** folder. Uses wand binding for 
imagemagick. you need wand 0.5.0; as of time of writing, 0.5.1 seemed to be broken & not working 
correctly. Only use if pillow isn't working for you, because ImageMagick was really finnicky especially 
on Ubuntu.

* **visiontranscription.py**: this batch-transcribes a folder of **pngs** and directs the output to a **txts** folder in the parent directory. Transcibes by sending a request to the google vision API for each image. **IMAGE FILE SIZES MUST BE SMALL** or google vision can't convert!

* **convert_and_vision_pillow.py**: this compiles both the above scripts (j2ktopng and visiontranscription) into one, using pillow.

* **convert_and_vision_wand.py**: compiles both the above scripts into one, using imagemagick and wand.

* **parsing.py**: takes a folder of .txts and parses them into .csv format with headers for first name, 
last name, publication, death date, etc. if a csv of the same name/location already exists, just appends new 
entries to this original file. outputs to a csv folder in the parent directory.

