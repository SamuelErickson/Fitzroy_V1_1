# -*- coding: utf-8 -*-
"""
Defines a function for sending email alerts. Don't call this script directly, import
into other scripts to add this functionality

For more explanation, see: https://www.afternerd.com/blog/how-to-send-an-email-using-python-and-smtplib/

"""


import smtplib

def sendEmailAlert(text = "This is a test of the email reporting system"):
    """ Takes an optional keyword "text" string argument, sends email with string as text. 
	"""
	
	address = "carpmasterrobot"
    password = "SmanskiLab2018"
    server = smtplib.SMTP_SSL('smtp.gmail.com',465) #,587, timeout=120)
    server.login(address,password)
    recipients = ["eric4204@umn.edu"] #list of email addresses
    server.sendmail(address,recipients, text)
    server.quit()


	# Below is alternative approach
    #server = smtplib.SMTP('smtp.gmail.com')	
    #server.connect("smtp.gmail.com")
    #server.ehlo()
    #server.starttls()
    #server.ehlo()
    #msg.as_string()


sendEmailAlert("This is a robot email: testing the CarpMaster emergency reporting system. You don't have to do anything about this. Direct questions to Sam Erickson.")
