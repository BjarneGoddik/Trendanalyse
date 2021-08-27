# -*- coding: utf-8 -*-
# Author: Morten Helmstedt. E-mail: helmstedt@gmail.com
""" This program extracts historical stock prices from Nordnet (and Morningstar as a fallback) """
 
import csv
import requests
from datetime import datetime
from datetime import date
from datetime import timedelta

# DATE AND STOCK DATA. SHOULD BE EDITED FOR YOUR NEEDS # 

# Symbol file name
filetxt='symbols.csv'

# Directory with stock data
datadir='./Rawdata/'

# Nordnet user account credentials
user = 'lurifax4180'
password = 'Skrammel-4180'

# Start date (start of historical price period)
startdate = '2019-01-01'

with open(filetxt) as csvfile:
	csv_reader = csv.reader(csvfile, delimiter=',')
	sharelist = list(csv_reader)
	csvfile.close()

#print (sharelist)

# List of shares to look up prices for.
# Format is: Name, Morningstar id, Nordnet stock identifier
# See e.g. https://www.nordnet.dk/markedet/aktiekurser/16256554-novo-nordisk-b
# (identifier is 16256554)
# All shares must have a name (whatever you like). To get prices they must
# either have a Nordnet identifier or a Morningstar id

# CREATE VARIABLES FOR LATER USE. #
 
# A cookie dictionary for storing cookies
cookies = {}
 
# NORDNET LOGIN #
 
# First part of cookie setting prior to login
url = 'https://classic.nordnet.dk/mux/login/start.html?cmpi=start-loggain&state=signin'
request = requests.get(url)
cookies['LOL'] = request.cookies['LOL']
cookies['TUX-COOKIE'] = request.cookies['TUX-COOKIE']
 
# Second part of cookie setting prior to login
url = 'https://classic.nordnet.dk/api/2/login/anonymous'
request = requests.post(url, cookies=cookies)
cookies['NOW'] = request.cookies['NOW']
 
# Actual login that gets us cookies required for later use
url = "https://classic.nordnet.dk/api/2/authentication/basic/login"
request = requests.post(url,cookies=cookies, data = {'username': user, 'password': password})
cookies['NOW'] = request.cookies['NOW']
cookies['xsrf'] = request.cookies['xsrf']
 
# Getting a NEXT cookie
url = "https://classic.nordnet.dk/oauth2/authorize?client_id=NEXT&response_type=code&redirect_uri=https://www.nordnet.dk/oauth2/"
request = requests.get(url, cookies=cookies)
cookies['NEXT'] = request.history[1].cookies['NEXT']
 
# LOOPS TO REQUEST HISTORICAL PRICES AT NORDNET

finalresult = ""
 
# Nordnet loop to get historical prices
for share in sharelist:
#	share[0] = "9001"
    # Nordnet stock identifier and market number must both exist
	finalresult = ""
	if int(share[0])<9000:
		print (share[0],share[1], share[2])
		url = "https://www.nordnet.dk/api/2/instruments/historical/prices/" + str(share[1])
		payload = {"from": startdate, "fields": "last"}
		data = requests.get(url, params=payload, cookies=cookies)
		jsondecode = data.json()
         
        # Sometimes the final date is returned twice. A list is created to check for duplicates.
		datelist = []
#		print (share[1], share[2])
		dateOld = date.today()-timedelta(days=1000)
		priceOld = "0,0"
		foerste=1
		for value in jsondecode[0]['prices']:
#            print (value)
			price = str(value['last'])
			price = price.replace(".",",")
			date = date.fromtimestamp(value['time'] / 1000)
#			datestr=datetime.strftime(date, '%Y-%m-%d')
#			date = datetime.strftime(date, '%Y-%m-%d')
#			print (date,dateOld)

			while date - dateOld > timedelta(days=1) and foerste==0:
				if (date-dateOld == timedelta(days=3)) and (dateOld.weekday()==4):
#					print "Weekend : "+str(dateOld) + " " + str(date)
					dateOld = date
				else:
					date_1 = dateOld+timedelta(days=1)
					if date_1.weekday()<5:
						if date_1 not in datelist:
							datelist.append(date_1)
							finalresult += '"' + str(date_1) + '"' + ";" + '"' + price + '"' + ";" + '"' + share[1] + '"' + "\n"
							print ("tilfoej en dag",str(date_1),",",str(date_1.weekday()))
					dateOld = date_1

            # Only adds a date if it has not been added before
			if date not in datelist:
				datelist.append(date)
#				print (datestr,price)
#				print('hej ',str(date) , price ,share[1])
				finalresult += '"' + str(date) + '"' + ";" + '"' + price + '"' + ";" + '"' + share[1] + '"' + "\n"
				priceOld = price
				dateOld = date
				foerste=0
		outfilename = datadir + str(share[0]) + ".csv"
#		print (finalresult)
		print (outfilename)
		with open(outfilename, "w") as fout:
			fout.write(finalresult)
		fout.close()
		finalresult = ""
		print ('File closed', outfilename)

# Morningstar loop to get historical prices is not used
         
for share in sharelist:
	finalresult = ""
	# Only runs for one specific fund in this instance
	if int(share[0])>9000:
		print (share[0],share[1], share[2])
		payload = {"id": share[1], "currencyId": "DKK", "idtype": "Morningstar", "frequency": "daily", "startDate": startdate, "outputType": "COMPACTJSON"}
		data = requests.get("http://tools.morningstar.dk/api/rest.svc/timeseries_price/nen6ere626", params=payload)
		jsondecode = data.json()
	
		datelist = []
		dateOld = datetime.today()-timedelta(days=1000)
		priceOld = "0,0"
		foerste=1

		for lists in jsondecode:
			price = str(lists[1])
			price = price.replace(".",",")
			date = datetime.fromtimestamp(lists[0] / 1000)
#			date = datetime.strftime(date, '%Y-%m-%d')
#			print (date,dateOld,timedelta(days=1), date-dateOld)
		
			while date - dateOld > timedelta(days=1) and foerste==0:
				if (date-dateOld == timedelta(days=3)) and (dateOld.weekday()==4):
#					print "Weekend : "+str(dateOld) + " " + str(date)
					dateOld = date
				else:
					date_1 = dateOld+timedelta(days=1)
					if date_1.weekday()<5:
						if date_1 not in datelist:
							datelist.append(date_1)
							finalresult += '"' + datetime.strftime(date_1, '%Y-%m-%d') + '"' + ";" + '"' + price + '"' + ";" + '"' + share[1] + '"' + "\n"
							print ("tilfoej en dag",str(date_1),",",str(date_1.weekday()))
					dateOld = date_1

            # Only adds a date if it has not been added before
			if date not in datelist:
				datelist.append(date)
				finalresult += '"' + datetime.strftime(date, '%Y-%m-%d') + '"' + ";" + '"' + price + '"' + ";" + '"' + share[1] + '"' + "\n"
				priceOld = price
				dateOld = date
				foerste=0

		outfilename = datadir + str(share[0]) + ".csv"
		print (outfilename)
		with open(outfilename, "w") as fout:
			fout.write(finalresult)
		finalresult = ""
		fout.close()

