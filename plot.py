# Plotting facilitet til investering 29.06.2020

import pandas as pd
from matplotlib import pyplot as plt

antal=700

#"16100293","sparinvest-index-globale-akt-m"
#"16099858","sparinvest-index-djsi-world-kl"
#"16099865","Sparvinvest-index-USA-Growth"
#"16099867","Sparvinvest-index-USA-value"
#"16099866","Sparvinvest-index-USA-smallcap"
#"16087488","sparindex-index-omx"
#"16102899","sparindex-index-emerging"
#"16099860","sparindex-index-europa-growth"
#"16099861","sparindex-index-europa-value"
#"16099859","sparindex-index-europa"

fil='./Filterdata/16087488.csv'
stockheader='sparindex-index-omx'
kursDF = pd.read_csv(fil, delimiter = ';', names=('date', 'lukkekurs', 'kursmeean50','kursmean200','kursexp'))
kursDF = kursDF.set_index(pd.DatetimeIndex(kursDF['date'].values))
kursDF = kursDF.sort_values(by=['date'], ascending=True)
kursDF = kursDF.tail(antal)
startkurs=kursDF.iat[1,4]
#kursDF2y = kursDF['lukkekurs']/startkurs
kursDF1y = kursDF['kursexp']/startkurs
kursDFx = kursDF['date']
plt.plot(kursDFx, kursDF1y,'k-', label=stockheader)
#plt.plot(kursDFx, kursDF2y,'r-', label=stockheader)

fil='./Filterdata/16100293.csv'
stockheader='sparinvest-index-globale-akt-m'
kursDF = pd.read_csv(fil, delimiter = ';', names=('date', 'lukkekurs', 'kursmeean50','kursmean200','kursexp'))
kursDF = kursDF.set_index(pd.DatetimeIndex(kursDF['date'].values))
kursDF = kursDF.sort_values(by=['date'], ascending=True)
kursDF = kursDF.tail(antal)
startkurs=kursDF.iat[1,4]
kursDF2y = kursDF['kursexp']/startkurs
kursDF2x = kursDF['date']
plt.plot(kursDFx, kursDF2y,'r-', label=stockheader)

fil='./Filterdata/16099865.csv'
stockheader='Sparvinvest-index-USA-Growth'
kursDF = pd.read_csv(fil, delimiter = ';', names=('date', 'lukkekurs', 'kursmeean50','kursmean200','kursexp'))
kursDF = kursDF.set_index(pd.DatetimeIndex(kursDF['date'].values))
kursDF = kursDF.sort_values(by=['date'], ascending=True)
kursDF = kursDF.tail(antal)
startkurs=kursDF.iat[1,4]
kursDF3y = kursDF['kursexp']/startkurs
kursDF2x = kursDF['date']
plt.plot(kursDFx, kursDF3y,'b-', label=stockheader)

fil='./Filterdata/16099866.csv'
stockheader='Sparvinvest-index-USA-smallcap'
kursDF = pd.read_csv(fil, delimiter = ';', names=('date', 'lukkekurs', 'kursmeean50','kursmean200','kursexp'))
kursDF = kursDF.set_index(pd.DatetimeIndex(kursDF['date'].values))
kursDF = kursDF.sort_values(by=['date'], ascending=True)
kursDF = kursDF.tail(antal)
startkurs=kursDF.iat[1,4]
kursDF4y = kursDF['kursexp']/startkurs
kursDF2x = kursDF['date']
plt.plot(kursDFx, kursDF4y,'c-', label=stockheader)

fil='./Filterdata/16102899.csv'
stockheader='sparindex-index-emerging'
kursDF = pd.read_csv(fil, delimiter = ';', names=('date', 'lukkekurs', 'kursmeean50','kursmean200','kursexp'))
kursDF = kursDF.set_index(pd.DatetimeIndex(kursDF['date'].values))
kursDF = kursDF.sort_values(by=['date'], ascending=True)
kursDF = kursDF.tail(antal)
startkurs=kursDF.iat[1,4]
kursDF5y = kursDF['kursexp']/startkurs
kursDF2x = kursDF['date']
plt.plot(kursDFx, kursDF5y,'m-', label=stockheader)

fil='./Filterdata/16099860.csv'
stockheader='sparindex-index-europa-growth'
kursDF = pd.read_csv(fil, delimiter = ';', names=('date', 'lukkekurs', 'kursmeean50','kursmean200','kursexp'))
kursDF = kursDF.set_index(pd.DatetimeIndex(kursDF['date'].values))
kursDF = kursDF.sort_values(by=['date'], ascending=True)
kursDF = kursDF.tail(antal)
startkurs=kursDF.iat[1,4]
kursDF6y = kursDF['kursexp']/startkurs
kursDF2x = kursDF['date']
plt.plot(kursDFx, kursDF6y,'g-', label=stockheader)

fil='./Filterdata/16099859.csv'
stockheader='sparindex-index-europa'
kursDF = pd.read_csv(fil, delimiter = ';', names=('date', 'lukkekurs', 'kursmeean50','kursmean200','kursexp'))
kursDF = kursDF.set_index(pd.DatetimeIndex(kursDF['date'].values))
kursDF = kursDF.sort_values(by=['date'], ascending=True)
kursDF = kursDF.tail(antal)
startkurs=kursDF.iat[1,4]
kursDF7y = kursDF['kursexp']/startkurs
kursDF2x = kursDF['date']
plt.plot(kursDFx, kursDF7y,'y-', label=stockheader)


#"16102899","sparindex-index-emerging"
#"16099860","sparindex-index-europa-growth"
#"16099861","sparindex-index-europa-value"
#"16099859","sparindex-index-europa"

plt.grid(axis = 'date', color='0.95')
plt.legend()
plt.show()

