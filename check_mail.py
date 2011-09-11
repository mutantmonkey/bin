#!/usr/bin/python3
#################################################################################
# check_mail.py - Check unread messages in all IMAP mailboxes
# based on http://www.doughellmann.com/PyMOTW/imaplib/
#
# author: Wade Duvall <wsduvall@amenrecluster.com>
# author: Doug Hellmann
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

import imaplib
import netrc
import re

server = 'cubensis.mutantmonkey.in'
port = 143

# get login info
nrc = netrc.netrc()
auth = nrc.authenticators(server)
username = auth[0]
password = auth[2]

list_response_regex = re.compile(b'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
unread_regex = re.compile(b"UNSEEN (\d+)")
unread_count = 0

# connect to server and login
conn = imaplib.IMAP4(server, port)
conn.starttls()
conn.login(username, password)

status, mailboxes = conn.list()

for mailbox_list_resp in mailboxes:
    flags, delim, mailbox = list_response_regex.match(mailbox_list_resp).groups()
    mailbox = mailbox.strip(b'"')
    if mailbox in (b'aur', b'bugs', b'cron', b'drafts', b'lists/novalug',
            b'lists/full-disclosure', b'lists/mappingdc', b'lists/opennic',
            b'lists/opennic/dns-operations', b'logwatch', b'shopping/deals',
            b'sent', b'spam'):
        continue
    mbox_status = conn.status(mailbox, '(UNSEEN)')[1][0]
    unread_match = unread_regex.search(mbox_status)
    if unread_match:
        unread_count += int(unread_match.group(1))

conn.logout()

print(unread_count, end='')

