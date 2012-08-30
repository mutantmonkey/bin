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
import os.path

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

# naively parse mutt mailboxes file
def parse_mailboxes():
    check_mailboxes = []
    with open(os.path.expanduser('~/.mutt/mailboxes.old'), 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) < 10:
                continue

            if line[0:9] == 'mailboxes':
                mailboxes = line[10:].split(' ')
                for m in mailboxes:
                    check_mailboxes.append(m[1:].encode('utf-8'))
    return check_mailboxes

#check_mailboxes = parse_mailboxes()

for mailbox_list_resp in mailboxes:
    flags, delim, mailbox = list_response_regex.match(mailbox_list_resp).groups()
    mailbox = mailbox.strip(b'"')
    if mailbox in (b'aur', b'bugs', b'cron', b'drafts', b'lists/cryptography',
            b'lists/cypherpunks', b'lists/novalug', b'lists/full-disclosure',
            b'lists/ipv6hackers', b'lists/liberationtech', b'lists/mappingdc',
            b'lists/opennic', b'lists/opennic/dns-operations',
            b'lists/oss-security', b'logwatch', b'shopping/deals', b'sent',
            b'spam', b'virginiatech/alumni-association',
            b'virginiatech/techsupport', b'virginiatech/wuvt'):
        continue
    mbox_status = conn.status(mailbox, '(UNSEEN)')[1][0]
    unread_match = unread_regex.search(mbox_status)
    if unread_match:
        unread_count += int(unread_match.group(1))

conn.logout()

f = open('/dev/shm/mail-mutantmonkey', 'w')
f.write(str(unread_count))
f.close()

#print(unread_count)
