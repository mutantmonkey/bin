#!/usr/bin/python3
################################################################################
# power_outages.py - script to scrape AEP outage data
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

import requests
import lxml.etree

state = "VA"
county = "Montgomery"

r = requests.get("https://www.aepcustomer.com/global/data/omsdata/OutageXML.aspx")
doc = lxml.etree.fromstring(r.text)
elem = doc.xpath('OperatingCo/state[@abbr="{state}"]/incident[@county="{county}"]'.\
        format(state=state, county=county.upper()))[0]

data = elem.attrib
data['county'] = county
data['state'] = state

print("{county}, {state}".format(**data))
print("Customers affected: {customers_affected} / {customers_served}".format(**data))
print("Repair issues: {repair_issues}".format(**data))
