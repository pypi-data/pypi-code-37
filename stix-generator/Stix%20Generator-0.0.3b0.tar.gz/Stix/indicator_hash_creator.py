"""

Description: Build a STIX Indicator document containing a File and relevant hash.

"""
# imports

import argparse
import hashlib 
import os
import sys

# python-cybox
from cybox.objects.file_object import File

# python-stix
import stix.utils as utils
from stix.core import STIXPackage, STIXHeader
from stix.indicator import Indicator
from stix.common import Confidence

# build arguments

parser = argparse.ArgumentParser(description='Build a STIX Indicator document containing a File observable with \
an associated hash')

parser.add_argument('--file', help='Target file for hashing', required=True)
parser.add_argument('--title', help='Title for entry', required=True)
parser.add_argument('--description', help='Description for entry', required=True)
parser.add_argument('--confidence', help='confidence value: High', required=True)
args = vars(parser.parse_args())


def hash_file(filename):
	if not os.path.exists(filename):
		print('Not Found: {}'.format(filename))
		sys.exit()
	hasher = hashlib.md5()
	with open(filename, 'rb') as afile:
		buf = afile.read()
		hasher.update(buf)
	return(hasher.hexdigest())	


def main(hash_value, title, description, confidence_value):
	# Create a CyboX File Object
	f = File()

	# This automatically detects that it's an MD5 hash based on the length
	f.add_hash(hash_value)

	# Create an Indicator with the File Hash Object created above.
	indicator = Indicator()
	
	indicator.title = title
	indicator.description = (description)
	indicator.confidence = confidence_value
	indicator.set_producer_identity("Information Security")
	indicator.set_produced_time(utils.dates.now())
	

	# Add The File Object to the Indicator. This will promote the CybOX Object
 	# to a CybOX Observable internally.
	indicator.add_object(f)

	# Create a STIX Package
	stix_package = STIXPackage()

	# Create the STIX Header and add a description.
	stix_header = STIXHeader()
	stix_header.description = description
	stix_package.stix_header = stix_header


	# Add our Indicator object. The add() method will inspect the input and
	# append it to the `stix_package.indicators` collection.
	stix_package.add(indicator)


	# Print the XML!
	with open('FileHash_indicator.xml', 'w') as the_file:
		the_file.write(stix_package.to_xml().decode('utf-8'))


if __name__ == '__main__':
	hash_value = hash_file(args['file'])
	title = args['title']
	confidence_value = args['confidence']
	description = args['description']
	main(hash_value, title, description, confidence_value)