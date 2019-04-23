# -*- coding: utf-8 -*-
"""
Defines a function for sending email alerts. Don't call this script directly, import
into other scripts to add this functionality

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
    recipients = ["carpmasterrobot@gmail.com","eric4204@umn.edu"]#"halvo432@umn.edu","tolo0007@umn.edu"]
    #recipients = ["carpmasterrobot@gmail.com","eric4204@umn.edu","bajer003@umn.edu","halvo432@umn.edu","hirt0021@umn.edu","hundt002@umn.edu"]
    server.sendmail("carpmasterrobot@gmail.com",recipients, text)
    server.quit()


sendEmailAlert("This is a robot email: testing the CarpMaster emergency reporting system. You don't have to do anything about this. Direct questions to Sam Erickson.")
