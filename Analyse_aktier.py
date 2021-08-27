#
# Analyse_aktier.py 2021.07.24
# Beregner exponentieltfilter af kursdata og normalisere dem med verdensmarkedsindekset.
#
import pandas as pd

symbolfil = 'symbols.csv'
strategifil = 'strategi.csv'
filterdir = './filterdata/'
databasedir = './Rawdata/'

def readsymbols(symbolfil):
	symbolDF = pd.read_csv(symbolfil, delimiter = ',', names=('nummer','nordnet_no', 'symbol','beskrivelse'))
	return symbolDF

def readfil(lfil,nantal):
	kursDF = pd.read_csv(lfil, delimiter = ';', names=('date', 'lukkekurs','nordnetno','kursexp','mean200','mean50','mean25','alfaexp'),decimal=',',parse_dates=True)
	kursDF = kursDF.sort_values(by=['date'], ascending=False)
	kursDF=kursDF.head(nantal)
	return kursDF

#
# Indlæser symbolliste
#   
symbolDF = readsymbols(symbolfil)
n=int(symbolDF.size/4)-1
#
# Henter normaliserede kursdata for det enkelte symbol 
# og kører det gennem filteret
#
aktielisteDF = pd.DataFrame()

for h in range(n-1):
	if 1999<symbolDF.iat[h, 0] < 3999:
		kursDF = pd.DataFrame()

		filtext3 = filterdir + str(symbolDF.iat[h, 0])+'.csv'
		kursDF=readfil(filtext3,200)
		nkursDF=int(kursDF.size/3)-1
		dage=5
		alfamean0= (kursDF.iat[0,5] - kursDF.iat[0+dage,5])/dage
		alfamean1= (kursDF.iat[0+1*dage,5] - kursDF.iat[2*dage,5])/dage

		delta = 0.005
	
		if  (kursDF.iat[0,1] > kursDF.iat[0,5]) and (alfamean0>delta) and (alfamean1>delta):
			tekst = 'Køb :'
		else:
			tekst = 'sælg:'
#	tekst=''
		if (kursDF.iat[0,1] > kursDF.iat[0,5]) and (kursDF.iat[5,1] < kursDF.iat[5,5]):
			tekst= '=>'+tekst
		elif (kursDF.iat[0,1] < kursDF.iat[0,5]) and (kursDF.iat[5,1] > kursDF.iat[5,5]):
				tekst= '=>'+tekst
		
		series_obj = pd.Series([tekst,kursDF.iat[0,1],symbolDF.iat[h, 3],kursDF.iat[0,5],alfamean0])
		aktielisteDF=aktielisteDF.append(series_obj, ignore_index=True)
pd.options.display.float_format = '{:.1f}'.format

aktielisteDF=aktielisteDF.sort_values(4,ascending=False)
print()
print('50 dages middelværdi under kursen sorteret på hældningenseneste '+str(dage)+' børsdage')
print(' Nederste 60 symboler')
print(aktielisteDF.iloc[:,0:4].tail(60))
print('Øverste 60 symboler:')
print(aktielisteDF.iloc[:,0:4].head(60))
print('Kolonne 0: køb/salg.  => er ændring seneste uge, kolonne 1 dagskurs, kolonne 3 50 dages middelkurs')
