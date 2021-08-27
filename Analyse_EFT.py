# -*- coding: utf-8 -*-#
# Analyse_ETF.py 2021.07.24
# for alle symboler i symbol.cas beregnes exponentieltfilter af kursdata, hældning over seneste 2 og 1 måned normaliseret med verdensmarkedsindekset (symbol 1000).
#
import pandas as pd

symbolfil = 'symbols.csv'
strategifil = 'strategi.csv'
filterdir = './filterdata/'
databasedir = './Rawdata/'

alfaworld=0
alfaworld2=0


def readsymbols(symbolfil):
	symbolDF = pd.read_csv(symbolfil, delimiter = ',', names=('nummer','nordnet_no', 'symbol','beskrivelse','type'))
	return symbolDF

def readfil(lfil):
	kursDF = pd.read_csv(lfil, delimiter = ';', names=('date', 'lukkekurs','nordnetno','kursexp','mean200','mean50','mean25','alfaexp'),decimal=',',parse_dates=True)
	kursDF = kursDF.sort_values(by=['date'], ascending=False)
#	kursDF = kursDF.head(280)
	return kursDF

#
# Indlæser symbolliste
#   
symbolDF = readsymbols(symbolfil)
n=int(symbolDF.size/5)
#n=20
print ('Antal indeks: ',n)
#
# Henter kursdata fra de filtrerede data
# Innitialisering
nvkursDF = pd.DataFrame()
ETFlisteDF = pd.DataFrame()
ETFud=pd.DataFrame()
ETFud4=pd.DataFrame()

i1=0
Beregningsdato = 1+3*0+20*0
tekst1 = pd.DataFrame()

for h in range(n-1):
#	print(h,symbolDF.iat[h, 0])
	kursDF = pd.DataFrame()
#	kursDFz = pd.DataFrame()
#	kursDFe = pd.DataFrame()
	testkursDF = pd.DataFrame()
	if (symbolDF.iat[h, 0] < 1999 or 9999>symbolDF.iat[h, 0]>3999) and symbolDF.iat[h,4]!='-':
#	if (symbolDF.iat[h, 0]) == 9001 or (symbolDF.iat[h, 0]) == 1000:

		# Indlæser kursdata for EFT symboler i "symbol.csv""
		filtext3 = filterdir + str(symbolDF.iat[h, 0])+'.csv'
		kursDF =  readfil(filtext3)
		dstart=kursDF.iat[Beregningsdato+20,0]
		dslut=kursDF.iat[Beregningsdato,0]
		nkursDF=int(kursDF.size/8)-1
		print ('EFT: ',h,filtext3,' Antal records: ',nkursDF)
		i1=i1+1
#		print (kursDF)
#
#	Bestemmer korrelationen mellem den eksp-mmidlede kurs og dagekursen. exp-midlede kurs er 18 dage efter dagskursen
#
		for nx in range(18,nkursDF):
			series_obj1=pd.Series([kursDF.iat[nx-18,1], kursDF.iat[nx,3]])
			testkursDF=testkursDF.append(series_obj1,ignore_index=True)
			testkursDF=testkursDF.head(228)
			tcorr=testkursDF[0].corr(testkursDF[1])
#
# Bestemmer væksten på 2 mdr (den styrende) og 1 mdr (korttidstrenden) fra expkursen
#   
		if (symbolDF.iat[h, 0]==1000):
			alfaworld=kursDF.iat[Beregningsdato,7]*100
			alfaworld2=kursDF.iat[Beregningsdato+20,7]*100
			alfaworldreel=(kursDF.iat[Beregningsdato,1]/kursDF.iat[Beregningsdato+20,1]-1)*100
#
# Udskriver hvis korrelationen er større end tcorr
#
		ETFud2=pd.DataFrame()
		ETFud3=pd.DataFrame()
		if tcorr > -1.0:
			series_obj2 = pd.Series([symbolDF.iat[h, 3], kursDF.iat[Beregningsdato,7]*100,(kursDF.iat[Beregningsdato,1]/kursDF.iat[Beregningsdato +20,1]-1)*100,(kursDF.iat[Beregningsdato,1]/kursDF.iat[Beregningsdato +5,1]-1)*100])
			ETFlisteDF=ETFlisteDF.append(series_obj2, ignore_index=True)
			for j in range (13*2):
				kursDF.iat[Beregningsdato+20*(j),0]
#				print ('j',j,kursDF.iat[Beregningsdato+20*(j),0] )
				series_obj1 = pd.Series([kursDF.iat[Beregningsdato+20*(j),0],symbolDF.iat[h, 3], kursDF.iat[Beregningsdato+20*j,7],(kursDF.iat[Beregningsdato+20*j,1]/kursDF.iat[Beregningsdato +20*(j+1),1]-1),kursDF.iat[Beregningsdato +20*(j+1),1],kursDF.iat[Beregningsdato+20*j,1]])
#			series_obj2 = pd.Series([symbolDF.iat[h, 3],symbolDF.iat[h, 0], kursDF.iat[Beregningsdato,7]*100,(kursDF.iat[Beregningsdato,1]/kursDF.iat[Beregningsdato +20,1]-1)*100,tcorr*100])
				ETFud2=ETFud2.append(series_obj1, ignore_index=True)
#		print (ETFud2)
#		ETFud3=ETFud2.sort_values(2,ascending=False)
#		ETFud3=ETFud3.head(5)
#		print (ETFud3)
		ETFud=ETFud.append(ETFud2)
# Udskriver resultetet
#print (kursDF)
pd.options.display.float_format = '{:.1f}'.format
#ETFlisteDF[2]=ETFlisteDF[2]-alfaworld
ETFud.columns='dato','ETF','Beregnet','Real -4','startkurs','slutkurs'
ETFlisteDF.columns='ETF','Beregnet','Real-4','Real-1'
#tekst1.columns='Trendanalyse'

ETFud ['ugenr']=pd.to_datetime(ETFud['dato']).dt.year*100+pd.to_datetime(ETFud['dato']).dt.week
#print (ETFud)
ETFud=ETFud.sort_values(['ugenr','Beregnet'],ascending=[False,False])
ETFlisteDF['Beregnet']=ETFlisteDF['Beregnet']-alfaworld

#print(i1,j)
#print (ETFlisteDF)
print(' ')
print('Udviklingen i verdensmarkedsindekset MSCI World fra ',dstart,' til ',dslut,':','{:.1f}%'.format(alfaworldreel), 'pr måned')
print('Relativ vækst for de forskellige indeks i  forhold til MSCI World (verdensmarkedsindekset). kolonne 2 er beregnede relative vækst for den kommende måned. Kolonne 3 er realiseret vækst for foregående måneden (som reference).')

print(ETFlisteDF.sort_values('Beregnet',ascending=False)) 


#Series_obj3=pd.Series(['Trendanalyse'])
#tekst1=tekst1.append(Series_obj3,ignore_index=True)

#Series_obj3=pd.Series(['============'])
#tekst1=tekst1.append(Series_obj3,ignore_index=True)
Series_obj3=pd.Series(['Beregningsdato '+dslut])
tekst1=tekst1.append(Series_obj3,ignore_index=True)
Series_obj3=pd.Series(['Udviklingen i verdensmarkedsindekset fra '+ dstart+' til '+dslut+' : '+'{:.1f}%'.format(alfaworldreel)])
tekst1=tekst1.append(Series_obj3,ignore_index=True)
Series_obj3=pd.Series(["."])
tekst1=tekst1.append(Series_obj3,ignore_index=True)

Series_obj3=pd.Series(['Relativ vækst for de forskellige indeks i forhold til MSCI World (verdensmarkedsindekset).'])
tekst1=tekst1.append(Series_obj3,ignore_index=True)
Series_obj3=pd.Series(['Kolonne 2 er beregnet relative vækst for den nye måned.'])
tekst1=tekst1.append(Series_obj3,ignore_index=True)
Series_obj3=pd.Series(['Kolonne 3 er realiseret vækst for de foregangne 4 uger (som reference)'])
tekst1=tekst1.append(Series_obj3,ignore_index=True)
Series_obj3=pd.Series(['Kolonne 4 er realiseret vækst for den foregangne uge (som reference)'])
tekst1=tekst1.append(Series_obj3,ignore_index=True)
Series_obj3=pd.Series(["."])
tekst1=tekst1.append(Series_obj3,ignore_index=True)
tekst1.columns=['Trendanalyse']

#
#Udskrivning af csv fil
#
tekst1.to_csv('weekperformance.csv', index = False, mode = 'w', header = True, encoding ='utf-8-sig')
ETFlisteDF.sort_values('Beregnet',ascending=False).to_csv('weekperformance.csv', index = False, header=True  , sep=';', decimal=',', mode='a')

#
#Udskrivning af html fil
#
htm1=ETFlisteDF.sort_values('Beregnet',ascending=False).to_html( index = False, header=True  , decimal=',',border="0", justify="left", formatters = {'Beregnet':'{:+4.1f}%'.format,'Real-4':'{:+4.1f}%'.format,'Real-1':'{:+4.1f}%'.format})
htm2=tekst1.to_html( index = False, border ="0",justify="left")

#htm2=ETFlisteDF.sort_values('Beregnet',ascending=False).to_html( index = False, header=True  , decimal=',')
# write html to file
text_file = open("weekperformence.html", "w")
text_file.write(htm2)
text_file.write(htm1)
text_file.close()

#ETFlisteDF.sort_values('Beregnet',ascending=False).to_csv(r'weekperformance.csv', index = False, header=True  ,sep=';', decimal=',', mode = 'a')


for k1 in range (j):
	for k2 in range(3):
		ETFud4=ETFud4.append(ETFud.iloc[k2+k1*i1])
#		print (k2+k1*i1,ETFud.iloc[k2+k1*i1])
#print (ETFud4)
#ETFud4=ETFlisteDF.sort_values(1,ascending=False)
ETFud4.to_csv (r'exportresult.csv', index = False, header=True  , sep=';', decimal=',')
