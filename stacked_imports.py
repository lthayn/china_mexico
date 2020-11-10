import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file = r'\hts2_data.xlsx'
folder = r'Z:\...'
link =  folder + file

vfolder=r'Z:\...'


#creating data set
post_wto = pd.read_excel(link,  sheet_name='2001_to_2019', converters={'hts2':str})

pre_1996_2000 = pd.read_excel(link,  sheet_name='1996_to_2000', converters={'hts2':str})

pre_1989_1995 = pd.read_excel(link,  sheet_name='1989_to_1995', converters={'hts2':str})

pre_wto = pre_1989_1995.merge(pre_1996_2000, how='outer', on=['hts2', 'ctryname', 'description'])

data = pre_wto.merge(post_wto, how='outer', on=['hts2', 'ctryname', 'description'])

data = data.drop(['hts2'], axis=1)
data = data.drop(['description'], axis=1)


grouped_data = data.groupby(['ctryname']).sum().reset_index('ctryname')

data_t = pd.melt(grouped_data, id_vars=['ctryname'], value_vars=[1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000,
                                                                 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011,
                                                                 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019])
data_t  = data_t .rename(columns={"variable": "year"})

data_p = data_t .pivot(index='year', columns='ctryname', values='value')

#creating million dollar values
data_p['ChinaM'] = data_p['China']/1000000000
data_p['MexicoM'] = data_p['Mexico']/1000000000
data_p['totalM'] = data_p['total']/1000000000
data_p['AllOtherM'] = data_p['totalM'] - ( data_p['ChinaM'] + data_p['MexicoM'] )

#figure

label = ['All other', 'China', 'Mexico']
color = ['b', 'r', 'g']
sns.set(style="darkgrid")
fig, ax = plt.subplots(figsize=(15, 7))


plt.stackplot(data_p.index, data_p.AllOtherM, data_p.ChinaM, data_p.MexicoM, labels=label, colors=color)
ax.set_ylabel('Imports for Consumption (Billions of US Dollars)');
ax.set_xlabel('Year');
plt.legend(loc='upper left', title='Countries')

#plt.show()
plt.savefig(vfolder + r'\stackedline_imp_consumption.png')

plt.close()

'''
data = pd.read_excel(link, converters={'hts8':str})

columns = ['description', 'wto']
data.drop(columns, inplace=True, axis=1)

grouped_data = data.groupby(['ctryname', 'year']).sum('value').reset_index('ctryname')

data_p = grouped_data.pivot_table(values='value', index='year', columns='ctryname')
'''