#!/usr/bin/python3
#################################################################################
# check_greader.py - Check unread posts in Google Reader
#
# author: jimmyorr@stackoverflow
# author: livibetter@stackoverflow
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

import urllib.parse
import urllib.request
import json
import netrc

# get login info
nrc = netrc.netrc()
auth = nrc.authenticators('google.com')
username = auth[0]
password = auth[2]

#cafile = '/etc/ssl/certs/GoogleInternetAuthority.pem'
cafile = '/usr/share/ca-certificates/mozilla/'\
        'Verisign_Class_3_Public_Primary_Certification_Authority.crt'

# Authenticate to obtain Auth
auth_url = 'https://www.google.com/accounts/ClientLogin'
auth_req_data = urllib.parse.urlencode({
        'Email': username,
        'Passwd': password,
        'service': 'reader'}, encoding='utf-8')
auth_req = urllib.request.Request(auth_url, data=bytes(auth_req_data,
    encoding='utf-8'))
# TODO: specify cafile or capath
auth_resp = urllib.request.urlopen(auth_req, cafile=cafile)
auth_resp_content = auth_resp.read()
auth_resp_dict = dict(x.split(b'=') for x in auth_resp_content.split(b'\n') if x)
authcode = str(auth_resp_dict[b"Auth"], encoding='ascii')

# Create a cookie in the header using the Auth
header = {}
header['Authorization'] = 'GoogleLogin auth={0}'.format(authcode)

reader_base_url = 'https://www.google.com/reader/api/0/unread-count?%s'
reader_req_data = urllib.parse.urlencode({
        'all': 'true',
        'output': 'json'})
reader_url = reader_base_url % (reader_req_data)
reader_req = urllib.request.Request(reader_url, None, header)
reader_resp = urllib.request.urlopen(reader_req, cafile=cafile)

data = str(reader_resp.read(), encoding='ascii')
data = json.loads(data)
if len(data['unreadcounts']) > 0:
    for obj in data['unreadcounts']:
        objid = obj['id'].split('/')
        if 'com.google' in objid and 'reading-list' in objid:
            count = int(obj['count'])
            print(count, end='')
else:
    print(0, end='')

