import sys
from xml.etree import ElementTree as ET

document = ET.parse(sys.argv[1])
ns = 'http://www.w3.org/1999/xhtml'
for page, i in enumerate(document.findall('.//{{{0}}}page'.format(ns))):
    for word in page.getchildren():
        octalescapedtext = ''.join(["\{0:o}".format(c) if c>127 else chr(c) for c in map(ord,word.text.encode('utf8'))])
        #escape quote character
        print octalescapedtext
