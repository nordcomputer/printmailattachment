#!/usr/bin/env python3
# prints and stores E-Mail Attachments

import datetime
import email
import getpass, imaplib
import os
import sys
import cups
import time
import locale
import shutil
import pprint
from bs4 import BeautifulSoup
from dotenv import load_dotenv


### Set your IMAP Serverdata and the printer name (you need a running cups server on your machine)
# load account credentials from env file
detach_dir = os.path.dirname(sys.argv[0])
dotenv_path = (detach_dir + '/.env')
load_dotenv(dotenv_path=dotenv_path)

userName = os.getenv('MAILUSERNAME')
passwd = os.getenv('MAILPASSWORD')
AllowedSenders = os.getenv('ALLOWEDSENDERS').split(',')
filenames = os.getenv('FILENAMES').split(',')
imap_server = os.getenv('IMAPSERVER')
Imapfolder = os.getenv('IMAPDIRECTORY')
soundfile=os.getenv('SOUNDFILE')
printer_name = os.getenv('PRINTERNAME')


if 'attachments' not in os.listdir(detach_dir):
    os.mkdir('attachments')


try:
    imapSession = imaplib.IMAP4_SSL(imap_server)
    typ, accountDetails = imapSession.login(userName, passwd)
    if typ != 'OK':
        print ('Not able to sign in!')
        raise
    imapSession.select(Imapfolder)
    typ, data = imapSession.search(None, 'UnSeen')
    if typ != 'OK':
        print ('Error searching Inbox.')
        raise

    # Iterating over all emails

    for msgId in data[0].split():

        typ, messageParts = imapSession.fetch(msgId, "(RFC822)")

        if typ != 'OK':
            print ('Error fetching mail.')
            raise

        emailBody = messageParts[0][1]
        mail = email.message_from_bytes(emailBody)



        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                def get_text(msg):
                    if msg.is_multipart():
                        return get_text(msg.get_payload(0))
                    else:
                        return msg.get_payload(None, True)
            string=get_text(mail)                           # string = E-Mail Text - maybe for later use...



        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            for val in AllowedSenders:
                if (val.lower() in mail['From'].lower()):
                    filePath = os.path.join(detach_dir, 'attachments', fileName)
                    if not os.path.isfile(filePath) :
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()

                        for val in filenames:
                            if val in fileName:
                                #os.system("mplayer "+ soundfile)                # comment in, if a sound should play, when a attachment gets printed
                                filePath1='attachments/'
                                conn = cups.Connection()
                                printers = conn.getPrinters()
                                conn.printFile (printer_name, filePath1+fileName, "", {})
                                print ('Attachment gets printed')

                        if not filenames:
                            #os.system("mplayer "+ soundfile)                # comment in, if a sound should play, when a attachment gets printed
                            filePath1='attachments/'
                            conn = cups.Connection()
                            printers = conn.getPrinters()
                            conn.printFile (printer_name, filePath1+fileName, "", {})
                            print ('Attachment gets printed')

            if len(AllowedSenders)==0:
                filePath = os.path.join(detach_dir, 'attachments', fileName)
                if not os.path.isfile(filePath) :
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()

                    for val in filenames:
                        if val in fileName:
                            #os.system("mplayer "+ soundfile)                # comment in, if a sound should play, when a attachment gets printed
                            filePath1='attachments/'
                            conn = cups.Connection()
                            printers = conn.getPrinters()
                            conn.printFile (printer_name, filePath1+fileName, "", {})
                            print ('Attachment gets printed')

                    if not filenames:
                        #os.system("mplayer "+ soundfile)                # comment in, if a sound should play, when a attachment gets printed
                        filePath1='attachments/'
                        conn = cups.Connection()
                        printers = conn.getPrinters()
                        conn.printFile (printer_name, filePath1+fileName, "", {})
                        print ('Attachment gets printed')


        imapSession.store(msgId, '+FLAGS', '\Seen')
    imapSession.close()
    imapSession.logout()
except :
    print ('There was an error during getting mails from the server.')
