import sys
from xml.etree import ElementTree as ET

document = ET.parse(sys.argv[1])
ns = 'http://www.w3.org/1999/xhtml'
corners = ['xMin', 'xMax', 'yMin', 'yMax']
# coordinates are in dpi, and computed from the top left corner
words = []
coords = []
for i, page in enumerate(document.findall('.//{{{0}}}page'.format(ns))):
    words.append([word.text for word in page.getchildren()])
    coords.append([tuple([float(word.attrib[c]) for c in corners]) for word in page.getchildren()])
