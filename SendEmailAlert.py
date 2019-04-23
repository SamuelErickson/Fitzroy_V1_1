# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 13:29:12 2018

@author: samue
"""


import smtplib

def sendEmailAlert(text = "This is a test of the email reporting system"):
    #https://www.afternerd.com/blog/how-to-send-an-email-using-python-and-smtplib/
    #server = smtplib.SMTP('smtp.gmail.com') #,587, timeout=120)
    server = smtplib.SMTP_SSL('smtp.gmail.com',465) #,587, timeout=120)
    server.login("carpmasterrobot", "SmanskiLab2018")
    #server.connect("smtp.gmail.com")
    #server.ehlo()
    #server.starttls()
    #server.ehlo()
    #msg.as_string()
    recipients = ["carpmasterrobot@gmail.com","eric4204@umn.edu"]
    server.sendmail("carpmasterrobot@gmail.com",recipients, text)
    server.quit()



