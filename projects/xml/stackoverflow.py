"""
http://stackoverflow.com/questions/28782864/modify-xml-file-using-elementtree
"""

import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element, SubElement

tree = ET.ElementTree(file='pricelist.xml')
root = tree.getroot()
pos = 0

# price - raise the main price and insert new tier
for elem in tree.iterfind('pricelist/item/price'):
    price = elem.text
    newprice = (float(price.replace(",", ".")))*1.2

    newtier = "NEW TIER"
    SubElement(root[0][pos][5], newtier)
    pos += 1

tree.write('pricelist-out.xml', "UTF-8")