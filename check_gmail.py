#!/usr/bin/python2
#################################################################################
# check_gmail.py - Check unread messages in Gmail Inbox using IMAP
#
# author: Wade Duvall <wsduvall@amenrecluster.com>
# author: mutantmonkey <mutantmonkey@gmail.com>
################################################################################

import keyring
import imaplib
import re

server = 'imap.gmail.com'
port = 993

username = 'mutantmonkey'
password = keyring.get_password(server, username)

mailbox = 'INBOX'

def store_password():
	import getpass

	password = getpass.getpass("Password for %s@%s: " % (username, server))
	keyring.set_password(server, username, password)

if not password:
	store_password()

# connect to server and login
conn = imaplib.IMAP4_SSL(server, port)
conn.login(username, password)

unread = re.compile("UNSEEN (\d+)")
unread_count = unread.search(conn.status(mailbox, '(UNSEEN)')[1][0]).group(1)
print int(unread_count)

conn.logout()

