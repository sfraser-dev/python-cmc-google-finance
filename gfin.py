#!/usr/bin/env python

# using Anaconda Python

# https://github.com/mrsmn/coinmarketcap-api
# https://pypi.python.org/pypi/forex-python

import sys
import pprint
import smtplib
import datetime
import json
import quandl

from forex_python.converter import CurrencyRates
myFx = CurrencyRates()

from email.mime.text import MIMEText

from googlefinance import getQuotes

def get_values_as_dict (longstring):
    myDict = {}
    # the coin info from coinmarket cap is a single long string
    for line in longstring.splitlines():
        if "[" not in line:
            if "{" not in line:
                if "}" not in line:
                    if "]" not in line:
                        # remove leading white space
                        noWhite = line.lstrip(' ')
                        noQuotes = noWhite.replace('"', '')
                        sp = noQuotes.split(":")
                        # remove leading white space
                        left = sp[0].lstrip(' ');
                        right = sp[1].lstrip(' ');
                        # remove commas
                        left = left.replace(',', '')
                        right = right.replace(',', '')
                        ## store in dictionary what is "left" and "right" of the equals sign
                        myDict[left] = right
    return myDict

def get_price_usd (longstring):
    myDict = get_values_as_dict(longstring)
    for key, value in myDict.items():
        if "price_usd" in key:
            return value

def get_market_vol (longstring):
    myDict = get_values_as_dict(longstring)
    for key, value in myDict.items():
        if "total_24h_volume_usd" in key:
            return value

def get_market_cap (longstring):
    myDict = get_values_as_dict(longstring)
    for key, value in myDict.items():
        if "total_market_cap_usd" in key:
            return value

def send_email (subject, body, to):
    sent_from = 'cmcwatcher@gmail.com'  
    #to = ['cmcwatcher@gmail.com','toepoke@hotmail.com'] 
    #to = ['toepoke@hotmail.com'] 
    #body = 'hope you get this\n\nregards,\n\nmr python'
    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login('cmcwatcher', 'Milhouse2214')
        server.sendmail(sent_from, to, email_text)
        server.close()
        print "email sent to: {}".format(to[0])
    except:
        print 'email failure!'

def get_price_from_cmc(dic, cable):
    usd = float(get_price_usd(coinmarketcap.ticker(dic['ticker'])))
    gbp = float(usd/cable)
    dic['usd']=usd
    dic['gbp']=gbp
    dic["curvalUsd"]=dic["abs"]*usd
    dic["curvalGbp"]=dic["abs"]*gbp

#myAllCoins = coinmarketcap.ticker()
#print myAllCoins

# get gbp/usd
cable   = float(myFx.get_rate('GBP','USD'))
chunnel = float(myFx.get_rate('EUR','GBP'))

# get date and time
now = datetime.datetime.now()
dateTime = now.strftime("%Y-%m-%d %H:%M")
email_body = "date and time: {}\n".format(dateTime)
email_body += "gbp/usd: {:.4f}\n".format(cable)
email_body += "eur/gbp: {:.4f}\n\n".format(chunnel)

print email_body

# quandl
print json.dumps(getQuotes('AAPL'), indent=2)
print json.dumps(getQuotes('MUTF_GB:VANG_LIFE_60_K6W1K3'), indent=2)
print json.dumps(getQuotes('MUTF_GB:VANG_FTSE_GLB_3GLTQB'), indent=2)
print json.dumps(getQuotes('MUTF_GB:VANG_LIFE_40_1UDNTWH'), indent=2)
print json.dumps(getQuotes('MUTF_GB:VANG_TARG_RETI_SIYUHH'), indent=2)

