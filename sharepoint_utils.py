from requests import Session
from zeep import Client
from zeep.transports import Transport
from requests_kerberos import HTTPKerberosAuth
import xml.etree.ElementTree as ET
from collections import OrderedDict
import pandas as pd
import sys
from zeep import xsd

reload(sys)
sys.setdefaultencoding('utf8')

# provide proxy if you are behind one
proxy = {
'http': "",
'https': "", }

session = Session()
session.verify = 'path to pem file'
session.auth=HTTPKerberosAuth()
session.proxies=proxy

# directory path to save the list data file
extract_dir=''
transport = Transport(session=session)

client = Client(
    'https://sharepoint.com/sites/<site_name>/_vti_bin/lists.asmx?WSDL',
    transport=transport)

def getList(listID):
    global client
    xml_out = client.service.GetList(listID)
    xml_tree = ET.ElementTree(xml_out[0])
    xml_root = xml_tree.getroot()
    col_map = dict()
    for cols in range(len(xml_root)):
        if 'ColName' in xml_root[cols].attrib.keys():
            col_map['ows_' + xml_root[cols].attrib['Name']] = xml_root[cols].attrib['DisplayName']
    return col_map

def getListItemChanges(listID,since):
    viewFields=xsd.SkipValue
    contains=xsd.SkipValue
    global client
    xml_out=client.service.GetListItemChanges(listID,viewFields,since,contains)
    xml_tree = ET.ElementTree(xml_out[0])
    xml_root = xml_tree.getroot()
    xml_row_count = int(xml_root.attrib['ItemCount'])
    xml_to_dict = dict()
    for row_number in range(xml_row_count):
        xml_row_dict = OrderedDict(xml_root[row_number].attrib)
        xml_to_dict[row_number] = dict(xml_row_dict)
    return xml_to_dict

def getCsv(xml_dict,listID,listName):
    global extract_dir
    list_df = pd.DataFrame.from_dict(xml_dict, orient='index')
    main_list_dict = getList(listID)
    missing_cols=list(set(main_list_dict.keys())-set(list_df.columns))
    for cols in missing_cols:
        list_df[cols]=pd.Series('NaN',index=list_df.index)
    list_df=list_df[sorted(list(set(main_list_dict.keys())))]
    fileName=extract_dir+listName+'.csv'
    list_df.to_csv(fileName,index=False)

# provide below string values
# ex: since='2018-12-02T23:38:18Z'
# listName='any friendly name used for saving the file'
# listID='ID enclosed in {}'

listName=''
listID=''
since=''
out_dict=getListItemChanges(listID,since)
getCsv(out_dict,listID,listName)
