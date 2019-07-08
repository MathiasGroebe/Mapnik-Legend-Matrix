#!/usr/bin/python
 
import sqlite3
from sqlite3 import Error
import xml.etree.ElementTree as ET
import re

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def select_all_rows(conn):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM mapnik_styles")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)

def insert_values(conn, values):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
 
    sql = ''' INSERT INTO mapnik_styles(LayerName, LayerMinScale, LayerMaxScale, StyleName, StyleFilter, RuleMinScale, RuleMaxScale, RuleFilter, RuleFilterEdit, RuleMarker)
              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, values)
    return cur.lastrowid        


def main():
    database = "mapnik.db"
 
    # create a database connection
    conn = create_connection(database)
    #read Mapnik file
    mapnikXML = ET.parse('osm_mapnik.xml')
    
    with conn:

        for layer in mapnikXML.getroot().findall("Layer"):
            layerValues = (layer.get("name"),
                     layer.get("minimum-scale-denominator"),
                     layer.get("maximum-scale-denominator"))
            for styleName in layer.findall("StyleName"):
                styleNameValues = (styleName.text.strip(),) 
                for style in mapnikXML.getroot().findall("Style"):
                    if style.get("name") == styleName.text.strip():
                        styleValues = (style.get("image-filters"),)

                        for rule in style.findall("Rule"):

                            scaleValue1 = ("",)
                            scaleValue2 = ("",)
                            filterValue = ""
                            symbolizerValues = ""
                            
                            for child in rule.iter():
                                if child.tag == "MinScaleDenominator":
                                    scaleValue1 = (child.text,)
                                if child.tag == "MaxScaleDenominator":
                                    scaleValue2 = (child.text,)
                                if child.tag == "Filter":
                                    filterValue = child.text.strip()
                                if child.tag == "PolygonSymbolizer":
                                    symbolizerValues = str(child.tag) + str(child.attrib) + "\n"
                                if child.tag == "LineSymbolizer":
                                    symbolizerValues = symbolizerValues + str(child.tag) + str(child.attrib) + "\n"
                                if child.tag == "MarkersSymbolizer":
                                    symbolizerValues = symbolizerValues + str(child.tag) + str(child.attrib) + "\n"
                                if child.tag == "ShieldSymbolizer":
                                    symbolizerValues = symbolizerValues + str(child.tag) + str(child.attrib) + "\n"
                                if child.tag == "LinePatternSymbolizer":
                                    symbolizerValues = symbolizerValues + str(child.tag) + str(child.attrib) + "\n"
                                if child.tag == "PolygonPatternSymbolizer":
                                    symbolizerValues = symbolizerValues + str(child.tag) + str(child.attrib) + "\n"
                                if child.tag == "RasterSymbolizer":
                                    symbolizerValues = symbolizerValues + str(child.tag) + str(child.attrib) + "\n"
                                if child.tag == "PointSymbolizer":
                                    symbolizerValues = symbolizerValues + str(child.tag) + str(child.attrib) + "\n"
                                if child.tag == "TextSymbolizer":
                                    symbolizerValues = symbolizerValues + str(child.tag) + str(child.attrib) + "\n"
                                if child.tag == "BuldingSymbolizer":
                                    symbolizerValues = symbolizerValues + str(child.tag) + str(child.attrib) + "\n"
                                if child.tag == "DotSymbolizer":
                                    symbolizerValues = symbolizerValues + str(child.tag) + str(child.attrib) + "\n"                                    
                                    
                            # Replace way_pixel and way_area
                            filterValueEdit = re.sub("and\s\(\[way_pixels]\s[<>=]+\s[0-9]+\)", "", filterValue)
                            filterValueEdit = re.sub("and\s\(\[way_area]\s[<>=]+\s[0-9]+\)", "", filterValueEdit)
                            ruleValues = scaleValue1 + scaleValue2 + (filterValue,) + (filterValueEdit,) + (symbolizerValues,)

                            
                            new_style = layerValues + styleNameValues + styleValues + ruleValues
                            #print(new_style, "\n")
                            #print(filterValue)
                            #print(re.sub("and\s\(\[way_pixels]\s[<>=]+\s[0-9]+\)", "", filterValue))
                
                            insert_values(conn, new_style)

                
            #select_all_rows(conn)
 
 
if __name__ == '__main__':
    main()

