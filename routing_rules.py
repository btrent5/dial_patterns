import argparse, datetime, shutil, pathlib, csv
from lxml import etree
from copy import deepcopy

# dial patterns

FILE_EXTENSION = '.xml'
DEBUG = True

parser = argparse.ArgumentParser(description='Generating routing rules for CS1K')
parser.add_argument('input_filename', help='Path to input file will determine format later')
parser.add_argument('-f', help='name for the output file, if not present will use the date')
args = parser.parse_args()

doc_number = 1
new_filename = str(datetime.date.today())

if args.f != None:
	new_filename = args.f

# never auto-overwrite data
dest = pathlib.Path(new_filename).with_suffix(FILE_EXTENSION)
while dest.exists():
	dest = pathlib.Path('{}_{}'.format(
		new_filename, doc_number)).with_suffix(FILE_EXTENSION)
	doc_number += 1

if DEBUG: print('output filename: {}'.format(dest))

# define schema
root = etree.Element('digitmapFullTOList')
root.append(etree.Element('implementationVersion'))
root.append(etree.Element('specificationVersion'))
root.append(etree.Element('buildNumber'))

pattern = etree.Element('DigitmapFullTO')
pattern.append(etree.Element('notes'))
pattern.append(etree.Element('deny'))
pattern.append(etree.Element('digitpattern'))
pattern.append(etree.Element('emergency_order'))
pattern.append(etree.Element('maxdigits'))
pattern.append(etree.Element('mindigits'))
pattern.append(etree.Element('routingoriginationName'))
pattern.append(etree.Element('routingpolicyNames'))
pattern.append(etree.Element('routingpolicyNames'))
pattern.append(etree.Element('routingpolicyNames'))
pattern.append(etree.Element('sipdomainName'))
pattern.append(etree.Element('treatasemergency'))
# assuming 3 routingpolicyNames


# fill version numbers with 0
for elem in root:
	elem.text = '0'

# does not account for missing/extra values in input file
# if missing/extra values exist, that policy will be invlaid
with open(pathlib.Path(args.input_filename)) as in_file:
	reader = csv.reader(in_file)
	for row in reader:
		if row[0] == 'notes':
			continue
		for i in range(len(row)):
			pattern[i].text = row[i]
		root.append(deepcopy(pattern))

with open(dest, 'wb') as out:
	out.write(etree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=True, with_tail=True, standalone=True))
