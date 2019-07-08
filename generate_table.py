# Script for generating a legend matrix
# Mathias Gröbe, TU Dresden 2019

#style = 'amenity-low-priority'
style = 'amenity%'
#style = 'admin%'


import time
import sqlite3
from sqlite3 import Error
import re
import string
import random
import imagesize # need to be install via pip
import xml.etree.ElementTree as ET

# https://pythontips.com/2013/07/28/generating-a-random-string/
def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def zoomlevelToScale(z): # converts the zoomlevel to scale number
    if z == 0:
        return 500000000
    if z == 1:
        return 250000000
    if z == 2:
        return 150000000
    if z == 3:
        return 70000000
    if z == 4:
        return 35000000
    if z == 5:
        return 15000000
    if z == 6:
        return 10000000
    if z == 7:
        return 4000000
    if z == 8:
        return 2000000
    if z == 9:
        return 1000000
    if z == 10:
        return 500000
    if z == 11:
        return 250000
    if z == 12:
        return 150000
    if z == 13:
        return 70000
    if z == 14:
        return 35000
    if z == 15:
        return 15000
    if z == 16:
        return 8000
    if z == 17:
        return 4000
    if z == 18:
        return 2000
    if z == 19:
        return 1000
	

def handleSymbolizer(text):
    example_symbol = ""
    polygonFlag = False

    # Flag for drawing a line around polygon, if an PolygonSymbolizer is present
    if "PolygonSymbolizer" in text:
        polygonFlag = True
    if "PolygonPatternSymbolizer" in text:
        polygonFlag = True

    # Convert rgba()
    #for rgba in re.findall("rgba\([0-9\s\.]+\)", text): 
     #    #text = text.replace(rgba, rgba.replace(" ",", "))
     #    #text = re.sub(rgba, re.sub(" ", ", ", rgba), text)



    for symbol in text.split("\n"):
        if "PolygonSymbolizer" in symbol:
            attributes = re.findall("{(.*)}", symbol)[0] #match attributes
            attributes = re.sub(",", "", attributes)
            attributes = re.sub(":", "=", attributes)

            for key in re.findall("'[a-zA-Z-]+'=", attributes): #remove ' for keys
                attributes = attributes.replace(key, key.replace("'",""))

            for rgba in re.findall("rgba\([0-9\s\.]+\)", attributes): #Convert rgba()
                attributes = attributes.replace(rgba, rgba.replace(" ",", "))

            dummy_area = "<polygon points ='5,5 55,5 55,55 5,55' " + attributes +  " />"
            example_symbol = example_symbol + dummy_area
            
        if "PolygonPatternSymbolizer" in symbol:
            attributes = re.findall("{(.*)}", symbol)[0] #match attributes
            attributes = re.sub(",", "", attributes)
            attributes = re.sub(":", "=", attributes)

            for key in re.findall("'[a-zA-Z-]+'=", attributes): #remove ' for keys
                attributes = attributes.replace(key, key.replace("'",""))

            fileTag = re.findall("file= '[a-zA-Z0-9\/_.]+'", attributes)[0]
            filePath = re.findall("'[a-zA-Z0-9\/_.]+'", fileTag)[0]
            
            width = 0
            height = 0

            if "svg" in filePath:
                try:
                    svg = ET.parse(filePath.replace("'", ""))

                    j = 1

                    for i in re.findall("[0-9]+", svg.getroot().get("viewBox")):
                        if j == 3:
                            height = i
                        if j == 4:
                            width = i
                        
                        j = j + 1
                except:

                    try:
                        svg = ET.parse(filePath.replace("'", ""))
                        width = svg.getroot().get("width")
                        height = svg.getroot().get("height")
                    except:
                        width = 32
                        height = 32
                        print("Error!", filePath)

            else:
                try:
                    width, height = imagesize.get(filePath.replace("'", ""))
                except:
                    print("Missing: ", filePath)        
            
            new_id = random_generator()

            pattern = '<defs><pattern id="' + new_id + '" patternUnits="userSpaceOnUse" width="' + str(width) + '" height="' + str(height) + '"><image xlink:href=' + filePath + ' x="0" y="0" width="' + str(width) + '" height="' + str(height) + '" /></pattern></defs>'
            dummy_area = pattern + "<polygon points ='5,5 55,5 55,55 5,55' fill= url(#" + new_id + ") />"
            example_symbol = example_symbol + dummy_area

        if "LineSymbolizer" in symbol:
            attributes = re.findall("{(.*)}", symbol)[0] #match attributes
            attributes = re.sub(",", "", attributes)
            attributes = re.sub(":", "=", attributes)

            for key in re.findall("'[a-zA-Z-]+'=", attributes): #remove ' for keys
                attributes = attributes.replace(key, key.replace("'",""))

            for rgba in re.findall("rgba\([0-9\s\.]+\)", attributes): #Convert rgba()
                attributes = attributes.replace(rgba, rgba.replace(" ",", "))                

            dummy_line = ""

            if polygonFlag:
                dummy_line = "<polyline points ='5,5 55,5 55,55 5,55 5,5' " + attributes +  " fill= 'none' />"
            else:
                dummy_line = "<line " + attributes +  " x1='5' y1='30' x2='55' y2='30'/>"

            example_symbol =  example_symbol + dummy_line
            #print(attributes)
            #print(dummy_line)
        
        if "MarkersSymbolizer" in symbol:
            attributes = re.findall("{(.*)}", symbol)[0] #match attributes
            attributes = re.sub(",", "", attributes)
            attributes = re.sub(":", "=", attributes)

            for key in re.findall("'[a-zA-Z-]+'=", attributes): #remove ' for keys
                attributes = attributes.replace(key, key.replace("'", ""))

            # Try to get radius
            radius = 0

            try:
                widthTag = re.findall(" width= '[0-9]+'", attributes)[0]
                widthNumber = re.findall("'[0-9.0-9]+'", widthTag)[0]
                radius =  re.sub("'", "", widthNumber)
            except:
                #print("Error", symbol)
                radius = 0

            # Try to find symbol
            dummy_symbol = ""
            width = 0
            height = 0
            color = ""

            try:
                fileTag = re.findall("file= '[a-zA-Z0-9\/_.]+'", attributes)[0]
                filePath = re.findall("'[a-zA-Z0-9\/_.]+'", fileTag)[0]
                #print(filePath)

                # Get color
                colorTag = re.findall("fill= '#[0-9a-z]+'", attributes)[0]
                colorNumber = re.findall("'#[0-9a-z]+'", colorTag)[0]
                color =  re.sub("'", "", colorNumber) 

                if "svg" in filePath:
                    try:
                        svg = ET.parse(filePath.replace("'", ""))

                        j = 1

                        for i in re.findall("[0-9]+", svg.getroot().get("viewBox")):
                            if j == 3:
                                height = i
                            if j == 4:
                                width = i
                            
                            j = j + 1
                    except:

                        try:
                            svg = ET.parse(filePath.replace("'", ""))
                            width = svg.getroot().get("width")
                            height = svg.getroot().get("height")
                        except:
                            width = 32
                            height = 32
                            #print("Error!", filePath)

                else:
                    try:
                        width, height = imagesize.get(filePath.replace("'", ""))
                    except:
                        print("Missing: ", filePath)

                dummy_symbol = "<image x = '30' y = '30' xlink:href= " + filePath + "width= '" + str(width) + "' height='" + str(height) + "'" + attributes + " style='fill:skyblue;'/>"
                #dummy_symbol = "<use xlink:href= " + filePath + "width= '" + str(width) + "' height='" + str(height) + "'/>"
            except:
                print("No file!")

            dummy_circle = "<circle cx = '30' cy = '30' r = '" + str(radius) + "' " + attributes + "/>"
            
            example_symbol =  example_symbol + dummy_circle + dummy_symbol

        if "TextSymbolizer" in symbol:
            attributes = re.findall("{(.*)}", symbol)[0] #match attributes
            attributes = re.sub(",", "", attributes)
            attributes = re.sub(":", "=", attributes)
            
            if "fontset-1" in attributes:
                attributes = attributes + "font-style = 'italic'"
            if "fontset-2" in attributes:
                attributes = attributes + "font-style = 'bold'"                

            # Replace fonts
            attributes = re.sub("fontset-[0-9]", "Noto Sans", attributes)
            attributes = re.sub("fontset-name", "font-family", attributes)
            attributes = re.sub("size", "font-size", attributes)

            for key in re.findall("'[a-zA-Z-]+'=", attributes): #remove ' for keys
                attributes = attributes.replace(key, key.replace("'",""))
            for rgba in re.findall("rgba\([0-9\s\.]+\)", attributes): #Convert rgba()
                attributes = attributes.replace(rgba, rgba.replace(" ",", "))                

            dummy_text = "<text x = '10' y = '30' " + attributes + " >Text sample</text>"
            example_symbol = example_symbol + dummy_text
      
    example_symbol = "<svg width='60px' height='60px' viewBox='0 0 60 60'>" + example_symbol + "</svg>"

    return example_symbol
            


db_path = 'mapnik.db'
conn = sqlite3.connect(db_path)

f = open('Legend-Matrix-' + style + '.html', 'w')

print("Create file.")
print("Creating content...")

start_time = time.time()

content1 = """
<html>
<head>
<title>Legend Matrix for """ + style + """</title>
<style>
body {
    font-family: monospace;
}
table {
  border-collapse: collapse;
  overflow: hidden;
}
table, th, td {
  border: 1px solid #aaa;
  padding: 6px;
  position: relative;
}


tr:hover {
  background-color: #eee;
}

td:hover::after {
    background-color: #eee;
    content: '';  
    height: 10000px;    
    left: 0;
    position: absolute;  
    top: -5000px;
    width: 100%;
    z-index: -1;
}

</style>
</head>
<body>
<h1>Legend Matrix</h1>
"""

content2 = """
    </body>
</html>"""
f.write(content1)

f.write("<table class = 'fixed_header'>\n")
f.write("<thead>\n")



data = (style,)

# Number of rows
c = conn.cursor()
c.execute("SELECT count(*) as cnt FROM (SELECT RuleFilterEdit FROM mapnik_styles WHERE StyleName LIKE ? GROUP BY RuleFilterEdit ORDER BY RuleFilterEdit)", data)
rownumber = c.fetchone()[0]


# Content for number of rows
c2 = conn.cursor()
c2.execute("SELECT RuleFilterEdit FROM mapnik_styles  WHERE StyleName LIKE ? GROUP BY  RuleFilterEdit ORDER BY RuleFilterEdit", data)


x = 21
y = int(rownumber)

f.write("<tr>")
f.write("<td>Style: " + style + "</td>")
f.write("<td>z0</td> <td>z1</td> <td>z2</td> <td>z3</td> <td>z4</td> <td>z5</td> <td>z6</td> <td>z7</td> <td>z8</td> <td>z9</td> <td>z10</td> <td>z11</td> <td>z12</td> <td>z13</td> <td>z14</td> <td>z15</td> <td>z16</td> <td>z17</td> <td>z18</td> <td>z19</td>")
f.write("</tr><tr>")
f.write("<td>Filter</td>")
f.write("<td>1:500,000,000</td> <td>1:250,000,000</td> <td>1:150,000,000</td> <td>1:70,000,000</td> <td>1:35,000,000</td> <td>1:15,000,000</td> <td>1:10,000,000</td> <td>1:4,000,000</td> <td>1:2,000,000</td> <td>1:1,000,000</td> <td>1:500,000</td> <td>1:250,000</td> <td>1:150,000</td> <td>1:70,000</td> <td>1:35,000</td> <td>1:15,000</td> <td>1:8,000</td> <td>1:4,000</td> <td>1:2,000</td> <td>1:1,000</td>")
f.write("</tr>")
f.write("</thead>")
f.write("<tbody>")

for i in range(1, y):
    f.write("<tr>")
    
    filterRule = str(c2.fetchone()[0])
    f.write("<td>" + filterRule + "</td>")
    for j in range(0, x-1):
        c3 = conn.cursor()
        z = zoomlevelToScale(j)
        c3.execute("SELECT RuleMarker, RuleFilter FROM mapnik_styles WHERE StyleName LIKE ? AND RuleFilterEdit = ? AND RuleMaxScale >= ? AND RuleMinScale <= ? AND LayerMaxScale >= ? AND LayerMinScale <= ?", (style, filterRule, z, z, z, z))
        #print(style)
        #print(filterRule)
        fetch = c3.fetchall()
        if fetch: # check if empty
            #handleSymbolizer(fetch[0][0])
            #f.write("<td>" + str(fetch[0][0]) + "</td>")    
            f.write("<td title='" + re.sub("'", "&apos;", fetch[0][0]) + "'>" + handleSymbolizer(fetch[0][0])+ "</td>")    
        else:
            f.write("<td>" + "</td>")    
            
    f.write("</tr>\n")

f.write("</tbody>")
f.write("</table>")

end_time = time.time()
run_time = end_time - start_time

print("Creation took ", str(round(run_time, 2)), "seconds.")

f.write(content2)
f.close()

print("File is written.")         
