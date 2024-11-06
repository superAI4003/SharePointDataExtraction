# SharePointDataExtraction
This is repository for data extraction from Sharepoint 2010 site using Python.

Basically Sharepoint exposes data via SOAP api, uses Kerberos authentication and for each site the WSDL files will be different.

Libraries used:
1) Zeep - Python SOAP Client
2) requests_kerberos - For kerberos authentication
3) xml.etree.ElementTree - For XML parsing
4) pandas - For csv conversion

Python version used: 2.7.15

For higher version, the print function change would do the needful

The below parameter is needed when you face SSL certificate error:
session.verify= 'ca pem file'
