#
# Plotting facilitet til aktier investering 21.07.2021
#
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
#plt.style.use('bmh')
symbolfil = 'symbols.csv'
filterdir='./Filterdata/'

def readsymbols(symbolfil):
	symbolDF = pd.read_csv(symbolfil, delimiter = ',', names=('nummer', 'F','symbol','beskrivelse'))
	return symbolDF

def readfil(lfil,nantal):
	kursDF = pd.read_csv(lfil, delimiter = ';', names=('date', 'lukkekurs','nordnetno','kursexp','mean200','mean50','mean25','alfaexp'),decimal=',',parse_dates=True)
	kursDF = kursDF.sort_values(by=['date'], ascending=False)
	kursDF=kursDF.head(nantal)
	return kursDF

def plot_fil(plotfil):
	global stockheader
	plotDF=pd.DataFrame()
	antal=300
#	print ('plotfil:',plotfil)
	for ct in range(1):
		c = int(plotfil)
		fil = filterdir + str(symbolDF.iat[c, 0])+'.csv'
		stockheader= str(symbolDF.iat[c,0])+' '+symbolDF.iat[c,3]
		kursDFz = readfil(fil,antal)
		if kursDFz.size/4>antal:
			if (1999<symbolDF.iat[c, 0]<3999):
				for acol in ['lukkekurs','mean200','mean50']:
					plotDF[acol]=kursDFz[acol]
					for j in range(0,antal):
						sk= kursDFz.iloc[antal-j-1].at[acol]
						plotDF.loc[j].at[acol]=sk
			else:
				for acol in ['lukkekurs','kursexp']:
					plotDF[acol]=kursDFz[acol]		
					for j in range(0,antal):
						sk= kursDFz.iloc[antal-j-1].at[acol]
						plotDF.loc[j].at[acol]=sk
			plotDF.plot(label=stockheader)

			tekst=str(symbolDF.iat[c, 3]) +' kurs for sidste ' +str(antal)+' dage'
			plt.title(tekst, fontsize = 18)
# plt.ylabel("relativ vaerdi", fontsize = 12)
			plt.xlabel("dato", fontsize = 12)

			plt.legend(fontsize = 8)
# plt.savefig('trendanalyse.pdf', orientation = 'landscape', format = 'pdf')
			plt.show()
		else:
			print ('plot ikke ok',antal, kursDFz.size/4)

symbolDF=readsymbols(symbolfil)
#
# antal: længde af plot interval 
#
nsymbolDF = int(symbolDF.size/4-1)
#print (nsymbolDF)
t1='aa'

while t1!='':
	t=input('l: list over symboler, p xx plot xx:')
	t1=t.strip().lower()
	if len(t1)>0:
		t2=t1[0]
	else:
		t2=t1
	if t2 == 'l':
		nantal=int(nsymbolDF/40)
		if nsymbolDF<40:
			print (symbolDF.iloc[:, 3])
		else:
			for j in range (nsymbolDF):
				print (j,' ',symbolDF.iloc[j, 0],symbolDF.iloc[j, 3])
	elif t2=='p':
		tm=int(t1[1:len(t)])
		if 0<=tm<nsymbolDF:
			plot_fil(tm)
	elif t2=='e':
		print('Programmet stopper')
		break


