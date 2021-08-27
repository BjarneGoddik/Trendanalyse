#
# filter_new.py
# Beregner exponentieltfilter af kursdata og normalisere dem med verdensmarkedsindekset.
#
import pandas as pd
import datetime
from datetime import date
from math import exp

symbolfil = 'symbols.csv'
strategifil = 'strategi.csv'
filterdir='./Filterdata/'
databasedir = './Database/'

def readsymbols(symbolfil):
	symbolDF = pd.read_csv(symbolfil, delimiter = ',', names=('nummer','nordnet_no', 'symbol','beskrivelse'))
	return symbolDF

def readfil(lfil):
	kursDF = pd.read_csv(lfil, delimiter = ';', decimal=',',names=('date', 'lukkekurs', 'kurs_symbol'))
#					  , parse_dates = True)
#	kursDF = kursDF.set_index(pd.DatetimeIndex(kursDF['date'].values))
	kursDF = kursDF.sort_values(by=['date'], ascending=False)
	return kursDF

#
# Dobbel Eksponentiet filter
#
def filter_exp16(kursDFz):
	nfiltersize = 95
	nkursDFz = int(kursDFz.size)
	y = [0.0]*nkursDFz
	f = [0.0]*nfiltersize
	d=16.0
	sf=0.0
	kursDF2 = kursDFz

	for n in range (0,nfiltersize):
		f[n]=exp(-n/d)-(exp(-n/d)*exp(-n/d))
		sf=f[n]+sf
	for n in range (0,nfiltersize):
		f[n]=f[n]/sf
	for nx in range (0,nkursDFz-nfiltersize):
		for j in range (0,nfiltersize-1):
			c=nx+j
			fx = f[j]*kursDFz.iat[c]
			y[nx] = y[nx] + fx
	return y
#
# Beregner hældningskoeficient for de seneste 40 dage (2 mdr)
#
def koeficient(kursDFz):
	nkursDFz = int(kursDFz.size)
	y = [0.0]*nkursDFz
	for nx in range (0,nkursDFz-1-40-75):
		if kursDFz.iat[nx+20] == 0:
			y[nx] =0
			print ('nx: ',nx,' kurs lig 0 ')
		else:
			y[nx]=(kursDFz.iat[nx]-kursDFz.iat[nx+40])/2/kursDFz.iat[nx+20]
	return y

#
# Indlæser symbolliste
#
symbolDF = readsymbols(symbolfil)
n=int(symbolDF.size/4)-1
verdensindexDF = pd.DataFrame(columns=['expworld'])
DF = pd.DataFrame()

#
# Henter normaliserede kursdata for det enkelte symbol
# og kører det gennem filteret
#

for c in range(n+1):
	kursDF = pd.DataFrame()
	rkursDF = pd.DataFrame()
	rrkursDF = pd.DataFrame()

	fil = databasedir + str(symbolDF.iat[c, 0])+'.csv'
	kursDF = readfil(fil)
	kursDFz = kursDF['lukkekurs']
	kursDF['expkurs'] = filter_exp16(kursDFz)
	rkursDF = kursDF.sort_values(by=['date'], ascending=True)
	rkursDF ['mean200'] =rkursDF['lukkekurs'].rolling(200).mean()
	rkursDF ['mean50'] =rkursDF['lukkekurs'].rolling(50).mean()
	rkursDF ['mean25'] =rkursDF['lukkekurs'].rolling(25).mean()
#	print (rkursDF.head(5))
	rrkursDF=rkursDF.sort_values(by=['date'], ascending=True)
#	print (rrkursDF.head(5))
	kursDF['mean200'] = rrkursDF ['mean200']
	kursDF['mean50'] = rrkursDF ['mean50']
	kursDF['mean25'] = rrkursDF ['mean25']

#	rkursDF['slope200']=rkursDF['mean200'].rolling('10').apply(lambda x: (x[-1]-x[0])/10)
#	n1=10
#	 df['slope_I'] = df['I'].rolling('600s').apply(lambda x: (x[-1]-x[0])/600)
	
#	print('Reverse DF ', rkursDF.tail(5))
#	print (kursDF.head(5))
#revkursDFz=kursDFZ.reversed
#    KursDFz200=revkurs.roling(200).mean()
	kursDFe = kursDF['expkurs']

#
# Lokalisere Verdensmarkedsindeks
#
	if symbolDF.iat[c,0] == 1000:
		verdensindexDF['expworld'] = kursDF['expkurs']
		verdenidag = verdensindexDF['expworld'].iat[1]
		verdensindexDF = verdensindexDF/verdenidag
#		print('Verdensindex fundet', c)
	DF['nycol'] = kursDF['expkurs']*verdensindexDF['expworld']

#	print (DF.head(5))
	kursDF['expkurs'] = DF['nycol']
#   n1=n
#    print (kursDF.head(5))

	kursDFe = kursDF['expkurs']
	kursDF['alfaexpkurs']= koeficient(kursDFe)

	filetext3 = filterdir + str(symbolDF.iat[c,0])+'.csv'
#    print ('Hej)
	print (filetext3, ' filen lukkes/skrives')
#	print (kursDF.head(5))

#    print ('hej')
	kursDF.to_csv(filetext3, index=False, header=False, sep=";",decimal=',')
