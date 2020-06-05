# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#%% Import what's needed
from markdown import markdown, markdownFromFile
import xml.etree.ElementTree as etree
import xml.dom.minidom as mnd
from extensions.iaea import ISI_Report, DelExtension

#%% Define the style
style = """
<style>
p {
	color: black;
	font-family: Times;
	font-size: 0.625em;
	text-align: justify;
	margin-left: 2mm;
	margin-right: 2mm;
	margin-top: 1.5mm;
}
td {
	color: black;
    border:0.5px solid black;
	font-family: Times;
	font-size: 0.625em;
	margin-left: 2mm;
	margin-right: 2mm;
	margin-top: 1.5mm;
}
th {
	color: black;
    border:0.5px solid black;
	font-family: Times;
	font-size: 0.625em;
    font-style: bold;
	margin-left: 2mm;
	margin-right: 2mm;
	margin-top: 1.5mm;
}
table {
       border:1px solid black;
       border-collapse: collapse;
       margin-left:auto;
       margin-right:auto;
}
li {
	color: black;
	font-family: Times;
	font-size: 0.625em;
	text-align: justify;
	margin-left: 2mm;
	margin-right: 2mm;
	margin-top: 1.5mm;
}
h1 {
	color: black;
	font-family: Times;
	font-size: 0.875em;
	text-align: justify;
	margin-left: 2mm;
	margin-right: 2mm;
	margin-top: 1.5mm;
}
h2 {
	color: black;
	font-family: Times;
	font-size: 0.750em;
	text-align: justify;
	margin-left: 2mm;
	margin-right: 2mm;
	margin-top: 1.5mm;
}
div.mainheading {
	color: black;
	font-family: Times;
	font-size: 0.875em;
	text-align: left;
	font-weight: bold;
}
div.subheading {
	color: black;
	font-family: Times;
	font-size: 0.625em;
	text-align: left;
	font-weight: bold;
}
</style>
"""
#%% Load the markdown text
mdfile = "/home/ishuwa/local/src/Python/ISI_QGIS/Tests/generic_text.md"

with open(mdfile, 'r') as f:
    dd = markdown(f.read(), extensions=['tables', DelExtension()])
    

#%% Define the XML file to write
xmlfile = "/home/ishuwa/local/src/Python/ISI_QGIS/Layouts/Central/central_analysis.qpt"
xmlfile = "/home/ishuwa/local/src/Python/ISI_QGIS/Layouts/East/LHS_layout.qpt"

#%% Parse the XML file
targetroot = etree.parse(xmlfile).getroot()

#%% Find the node for the main text
li = targetroot.find(".//LayoutItem[@id='Main text body']")
li.set("labelText", style+dd)

#%% Pretty print the XML and write back to file
pxml = mnd.parseString(etree.tostring(targetroot, 'utf-8').decode().replace('\n','').replace('\t',''))
with open(xmlfile, 'w') as f:
    f.write(pxml.toprettyxml())