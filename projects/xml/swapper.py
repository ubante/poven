#!/usr/bin/env python

"""
http://stackoverflow.com/questions/1591579/how-to-update-modify-a-xml-file-in-python
http://stackoverflow.com/questions/6523886/find-and-replace-values-in-xml-using-python
"""

import re
import xml.etree.ElementTree as ET

# Read it in.
print("Reading....")
file = "sample.xml"
tree = ET.parse(file)

# Swapparoo.
tree.find('timeperd/timeinfo/rngdates/begdate').text = '1/1/2011'
tree.find('timeperd/timeinfo/rngdates/enddate').text = '1/1/2011'

# Change the tag from monster-old to monster-new
current_element = tree.find('things/monster/source')
current_text = current_element.attrib["file"]
# future_text = "future_string"

future_text = re.sub("monster-old", "monster-new", current_text)
print("Changing {} to {}".format(current_text, future_text))
current_element.attrib["file"] = future_text

# Addaroo to root.
root = tree.getroot()
new_tag = ET.SubElement(root, 'a')
new_tag.text = 'body text'
new_tag.attrib['x'] = '1'  # must be str; cannot be an int
new_tag.attrib['y'] = 'abxd'

# Write it out.
tree.write("new.xml")
