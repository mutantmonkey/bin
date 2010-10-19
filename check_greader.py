#!/usr/bin/python2
#################################################################################
# check_greader.py - Check unread posts in Google Reader
#
# author: jimmyorr@stackoverflow
# author: livibetter@stackoverflow
# author: mutantmonkey <mutantmonkey@gmail.com>
################################################################################

import urllib, urllib2
import json
import keyring

username = 'mutantmonkey@gmail.com'
password = keyring.get_password('google.com', username)

def store_password():
	import getpass

	password = getpass.getpass("Password for %s: " % username)
	keyring.set_password('google.com', username, password)

if not password:
	store_password()

# Authenticate to obtain Auth
auth_url = 'https://www.google.com/accounts/ClientLogin'
auth_req_data = urllib.urlencode({'Email': username,
                                  'Passwd': password,
                                  'service': 'reader'})
auth_req = urllib2.Request(auth_url, data=auth_req_data)
auth_resp = urllib2.urlopen(auth_req)
auth_resp_content = auth_resp.read()
auth_resp_dict = dict(x.split('=') for x in auth_resp_content.split('\n') if x)
# SID = auth_resp_dict["SID"]
AUTH = auth_resp_dict["Auth"]

# Create a cookie in the header using the Auth
header = {}
header['Authorization'] = 'GoogleLogin auth=%s' % AUTH

reader_base_url = 'http://www.google.com/reader/api/0/unread-count?%s'
reader_req_data = urllib.urlencode({'all': 'true',
                                    'output': 'json'})
reader_url = reader_base_url % (reader_req_data)
reader_req = urllib2.Request(reader_url, None, header)
reader_resp = urllib2.urlopen(reader_req)

data = json.loads(reader_resp.read())
if len(data['unreadcounts']) > 0:
	for obj in data['unreadcounts']:
		objid = obj['id'].split('/')
		if 'com.google' in objid and 'reading-list' in objid:
			print int(obj['count'])
else:
	print 0

