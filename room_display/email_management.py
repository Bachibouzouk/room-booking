# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 22:32:32 2016

@author: pfduc
"""

import smtplib
import hashlib




MCGILL_SERVERS =['mail.mcgill.ca', 'mcgill.ca']

def send_email(recipient, subject, body,
               user = "softbooking@physics.mcgill.ca", pwd = None):

    gmail_user = user
    
    gmail_pwd = pwd
        
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    
		#here we should use smtp.mcgill.ca or something similar
    if not gmail_pwd is None:
        
        try:
            
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            print('successfully sent the mail to %s'%(recipient))
            
        except:
            
            print("failed to send mail to %s"%(recipient))

    else:
        
#        try:
        #mailhost.mcgill.ca
        server = smtplib.SMTP("mx0.physics.mcgill.ca", 25)
        server.sendmail(FROM, TO, message)
        server.close()
        print("successfully sent the mail to %s"%(recipient))
            
#        except:
#            
#            print("failed to send mail to %s"%(recipient))
            

def send_encrypted_link(email, information, title, key, link):
    
    act_key = hashlib.sha256(key.encode() + information.encode()).hexdigest()
    link="%s%s"%(link,act_key)
    print(link)
    send_email(email,title,link)     
                    
def check_encription(hashed_value, value,salt):
    """returns true if the value and the hashed values are identical after hashing of the value """
    return hashed_value == hashlib.sha256(salt.encode() + value.encode()).hexdigest()
                         
                    
            
def is_from_mcgill(email):
    
    #if email is a list of emails
    if hasattr(email, '__iter__') and not isinstance(email,str):

        emails = email
        answers = []
        for email in emails:
            answers.append(is_from_mcgill(email))
        return answers
    
    else:
        msg = None
        if '@' in email:
            uname, server = email.split('@')
            if server in MCGILL_SERVERS:

                    
                if "." in uname:
                    firstname, lastname = uname.split(".")
                    
                    if firstname == "":
                        msg = "the firstname is empty"
                    elif lastname == "":
                        msg = "the lastname is empty"
                    else:
                        pass
                else:
                    msg = "not in the format 'firstname.lastname'"

            else:
                msg = "server incorrect"
        else:
            msg = "not a valid email address, @ missing"
            raise ValueError(msg)
        
        if msg == None:
            return True
        else:
            msg = "%s is an invalid email address : "%(email) + msg
            print(msg)
            return False
if __name__ == "__main__":
    
    print(is_from_mcgill([".@mail.mcgill.ca",".e@mail.mcgill.ca","a.@mail.mcgill.ca","a.b@mail.mcgill.ca","@mail.mcgill.ca","a@mail.mcgill.ca","pfduc@mcgill.ca","132@mcgill.ca"]))
    
    send_email("pfduc@physics.mcgill.ca","test","haha")