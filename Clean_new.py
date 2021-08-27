# -*- coding: utf-8 -*-
# 
##############################################################################
# clean 2021.07.24
##############################################################################
# Bruger filen symbol.csv og udbytte.csv
# Flytter data fra Rawdata/ til Database/
# korrektion for udbytter (udbytte.csv)
# Ændret sorteringsrækkefølgen på udbyttefilen
# Ændret DB nummer til internt
#

#import csv
#import datetime
#from datetime import date, timedelta
import pandas as pd

try:
	datadir = './Rawdata/'
	databasedir = './Database/'

	filetxt = 'udbytte.csv'

	udbytteF = pd.read_csv(filetxt,delimiter=',',names=['symbol_number', 'Udbytte', 'udbyttedate','d'])
	udbytteF = udbytteF.sort_values(by=['symbol_number','udbyttedate'], ascending=True)
	print (udbytteF)

	filetxt2 = 'symbols.csv'
	symbolF = pd.read_csv(filetxt2,delimiter=',',decimal=',',names=['symbol_number','nordnet_nummer', 'd','beskrivelse'])
	symbolF = symbolF.sort_values(by=['symbol_number'], ascending=True)
	nsymbol = symbolF.size/2
	print (symbolF)
	
#	print ('DF size: ',int(symbolF.size/3))

	for i in range(int(symbolF.size/4)):
#		print ('i= :',i)
		filetext3 = datadir + str(symbolF.iat[i,0])+'.csv'
		print (filetext3, ' Filen aabnes,',str(symbolF.iat[i,3]))
		kursF = pd.read_csv(filetext3,delimiter=';',decimal=',',names=['kursdate','kurs','d'], dtype={"kurs":"float64"})
		kursF = kursF.sort_values(by=['kursdate'], ascending=False)
		print (kursF.head(5))
		
		j=0
		k=0
		while int(udbytteF.iat[j,0]) < int(symbolF.iat[i,0]) and (j< udbytteF.size/4 -1) :
			j +=1
#			print (udbytteF.iat[j,0],' ',symbolF.iat[i,0])
		while udbytteF.iat[j,0] == symbolF.iat[i,0]and (j< udbytteF.size/4 -1):
			k +=1
			print ("Udbytte: " +str(k)) 
			udbytte=-udbytteF.iat[j,1]
			udbyttedato=udbytteF.iat[j,2]
			udbyttefilnavn=udbytteF.iat[j,0]
			print (udbyttefilnavn,udbytte,udbyttedato)
			print (symbolF.iat[i,0], ' Data aendres')

			kursF.loc[kursF['kursdate']<=udbyttedato, 'kurs'] +=udbytte 
			j +=1
		if int(udbytteF.iat[j,0]) < int(symbolF.iat[i,0]) and (j< udbytteF.size/4 -1):
			j = 0
		filetext3 = databasedir + str(symbolF.iat[i,0])+'.csv'
		print (filetext3, ' filen lukkes/skrives')
#		print (kursF.head(5))
		kursF.to_csv(filetext3, index=False, header=False, sep=";",decimal=',')
		k=0
		j=0
		
		print (" ")
except Exception as ex:
	print ('Error!',ex)
finally:
	print ('Execcution ended')