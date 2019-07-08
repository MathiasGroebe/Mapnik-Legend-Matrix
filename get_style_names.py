import xml.dom.minidom

mydoc = xml.dom.minidom.parse('osm_mapnik.xml')

for node in mydoc.getElementsByTagName("Style"):
    print(node.getAttribute("name"))

