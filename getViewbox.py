import xml.etree.ElementTree as ET
import re

svg = ET.parse('symbols/leaftype_needleleaved.svg')

height = 0
width = 0
j = 1

for i in re.findall("[0-9]+", svg.getroot().get("viewBox")):
    if j == 3:
        height = i
    if j == 4:
        width = i
    
    j = j + 1

print(height)
print(width)



#print(svg.getroot().find("svg"))

#print(svg.write)