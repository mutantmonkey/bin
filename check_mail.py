#!/usr/bin/python2
#################################################################################
# check_mail.py - Check unread messages in all IMAP mailboxes
# based on http://www.doughellmann.com/PyMOTW/imaplib/
#
# author: Wade Duvall <wsduvall@amenrecluster.com>
# author: Doug Hellmann
# author: mutantmonkey <mutantmonkey@gmail.com>
################################################################################

import keyring
import imaplib
import re

server = 'cubensis.mutantmonkey.in'
port = 993

username = 'mutantmonkey@mutantmonkey.in'
password = keyring.get_password(server, username)

unread_count = 0

list_response_regex = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
unread_regex = re.compile("UNSEEN (\d+)")

def store_password():
	import getpass

	password = getpass.getpass("Password for %s@%s: " % (username, server))
	keyring.set_password(server, username, password)

if not password:
	store_password()

# connect to server and login
conn = imaplib.IMAP4_SSL(server, port)
conn.login(username, password)

status, mailboxes = conn.list()

for mailbox_list_resp in mailboxes:
	flags, delim, mailbox = list_response_regex.match(mailbox_list_resp).groups()
	mailbox = mailbox.strip('"')
	if mailbox in ('lists/novalug', 'lists/full-disclosure', 'logwatch', 'shopping/deals', 'sent', 'spam'):
		continue
	mbox_status = conn.status(mailbox, '(UNSEEN)')[1][0]
	unread_match = unread_regex.search(mbox_status)
	if unread_match:
		unread_count += int(unread_match.group(1))

conn.logout()

print unread_count

