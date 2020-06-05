from qgis.core import *
import qgis.utils
import os
import re
import xml.etree.ElementTree as etree

#%% Cell
""" Function to join stuff """
def commaAndJoin(stringList):
    if len(stringList) <= 2:
        return ' and '.join(stringList)
    else:
        return commaAndJoin([', '.join(stringList[:-1]), stringList[-1]])
        
#%% Cell
""" Load the satellite vendors xml file """
xmldoc = etree.parse(u'//sg.info/SGIM/Data/ISI/ISI_Public/Projects/Ishuwa/ArcPro Template/Python/SatVend.xml')
xmlroot = xmldoc.getroot()
sensorsXML = xmlroot.findall("asset")
sensorDictionary = [[[abb.text for abb in asset], 
                      asset.get("sensor"), 
                      asset.get("vendor")] for asset in sensorsXML]
                      

#%% Cell
""" Setup the a dictinoary of months """
# Setup a month dictionary
mDict = {'01': 'Jan', 
         '02': 'Feb', 
         '03': 'Mar', 
         '04': 'Apr', 
         '05': 'May', 
         '06': 'Jun', 
         '07': 'Jul', 
         '08': 'Aug', 
         '09': 'Sep', 
         '10': 'Oct', 
         '11': 'Nov', 
         '12': 'Dec'}
         
def updateLayout(layoutName):
    #%% Cell
    """ Get the layouts associated with this project """
    myLyt = QgsProject.instance().layoutManager().layoutByName('My First')

    #%% Cell
    """ Get a list of map items in the layer """
    mapItems = [m for m in myLyt.items() if isinstance(m, QgsLayoutItemMap)]

    #%% Cell
    """ Get the layer sources for each map item """
    mapLayers = [[(mItem.displayName(), m.dataProvider().dataSourceUri()) 
                  for m in mItem.layers() if isinstance(m,QgsRasterLayer)][0] 
                  for mItem in mapItems]

    #%% Cell
    """ Get all tif and img file types """
    rasterFiles = [(f[0], os.path.split(f[1])[-1]) 
                   for f in mapLayers if ".tif" in f[1] or ".img" in f[1]]
                   
    #%% Cell
    """ Now extract what we need from the file name """
    signatureFilters = ['[0-9]{8}_.*_.*_[0-9]*', 
                        '[0-9]{8}T[0-9]{6}[A-Z]{2}_[0-9A-Za-z]*_']
    metaData = [[(x[0], re.findall(signature, x[1])) for x in rasterFiles]
                 for signature in signatureFilters]

    opticalImages = [m[0] for m in metaData if len(m[0][1]) > 0]
    radarImages = [m[1] for m in metaData if len(m[1][1]) > 0]

    allMetaData = [(m[0], [mm.split("_") for mm in m[1]]) for m in radarImages + opticalImages]
    allDateData = [(m[0], ' and '.join(["%s %s %s" % (x[0][6:8], mDict[x[0][4:6]], x[0][0:4]) 
                            for x in m[1]])) for m in allMetaData]

    #%% Cell
    """ Put stuff in the assets dictionary """
    mapSensors = [x for y in [[m[1] for m in n[1]] for n in allMetaData] for x in y]
    mapSensors = list(set(mapSensors))
    assets = [x for x in sensorDictionary for m in mapSensors if m in x[0]]

    #%% Cell
    """ Get the sensors and vendors of the imagery """
    sensors = list(set([s[0][1] for s in assets if len(s) > 0]))
    vendors = list(set([s[2] for s in assets if len(s) > 0]))
    CopyrightText = """
    <style>
        p.copyright {
            font-weight: bold;
            font-family: Arial, sans-serif;
            line-height: 1;
            font-size: 1em;
            letter-spacing: -0;
        }
    </style>
    <p class="copyright">%s<br>Contains %s Copyright Materials</p>
    """
    copyright = CopyrightText % (commaAndJoin(sensors), commaAndJoin(vendors))

    #%% Cell
    """ See if we can find the copyright item """
    copyright_item = lyt.itemById("Copyright")
    if copyright_item is not None:
        copyright_item.setText(copyright)
        
    #%% Cell
    """ See if we can update the date labels """
    DateText = """
    <style>
        span.date {
            font-weight: bold;
            font-family: Arial, sans-serif;
            line-height: 1;
            font-size: 1em;
            background-color: white;
        }
    </style>
    <span class="date">&thinsp;%s&thinsp;</span>
    """
    for candidate in allDateData:
        candidate_item = lyt.itemById(candidate[0] + "Date")
        if candidate_item is not None:
            candidate_item.setText(DateText % candidate[1])