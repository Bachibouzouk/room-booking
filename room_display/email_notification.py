# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 22:32:32 2016

@author: pfduc
"""

import smtplib

def send_email(pwd, recipient, subject, body, user):

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
		#here we should use smtp.mcgill.ca or something similar
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail to %s'%(recipient))
    except:
        print("failed to send mail to %s"%(recipient))
    