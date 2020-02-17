import os
import re

for filename in os.listdir('.'):
	if filename in ['.DS_Store', 'namefix.py']:
		continue
	name = filename.split(" ")
	firstname = name[1].split(".")[0]
	lastname = name[0].split(",")[0]
	new_filename = lastname + "-" + firstname + ".jpg"

	os.rename(filename, new_filename)