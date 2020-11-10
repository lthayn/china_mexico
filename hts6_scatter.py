import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

folder=r'Z:\...'
vfolder=r'Z:\...'

post_wto = pd.read_excel (folder + r'\hts6_data.xlsx', sheet_name='2001_to_2019',
                             converters={'hts6':str})
post_wto_2 = pd.melt(post_wto, id_vars=['ctryname', 'hts6', 'description'], value_vars=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
                                                                                        2013, 2014, 2015, 2016, 2017, 2018, 2019])
post_wto_2 = post_wto_2.rename(columns={"variable": "year"})


pre_1996_2000 = pd.read_excel (folder + r'\hts6_data.xlsx', sheet_name='1996_to_2000',
                             converters={'hts6':str})

pre_1989_1995 = pd.read_excel (folder + r'\hts6_data.xlsx', sheet_name='1989_to_1995',
                             converters={'hts6':str})


pre_wto = pre_1989_1995.merge(pre_1996_2000, how='outer', on=['ctryname', 'hts6', 'description'])


pre_wto_2 = pd.melt(pre_wto, id_vars=['ctryname', 'hts6', 'description'], value_vars=[1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000])
pre_wto_2 = pre_wto_2.rename(columns={"variable": "year"})
#pre_wto_2["wto"] = 0


data = pd.concat([post_wto_2, pre_wto_2])
data = data.drop(['description'], axis=1)

#print(data.columns)

data_p = data .pivot(index=['year', 'hts6'], columns='ctryname', values='value').reset_index()
data_p= data_p.fillna(0)

#creating million dollar values
data_p['ChinaM'] = data_p['China']/1000000
data_p['MexicoM'] = data_p['Mexico']/1000000
data_p['totalM'] = data_p['total']/1000000
#creating percentages
data_p['China_per'] = data_p['China']/data_p['total']*1000
data_p['Mexico_per'] = data_p['Mexico']/data_p['total']*1000

'''
China = data_p[['year', 'hts6', 'China', 'ChinaM', 'China_per']]
China = China.rename(columns={"China": "value", "ChinaM": "valueM", "China_per": "percent"})
China['ctryname']='China'

Mexico = data_p[['year', 'hts6', 'Mexico', 'MexicoM', 'Mexico_per']]
Mexico = Mexico.rename(columns={"Mexico": "value", "MexicoM": "valueM", "Mexico_per": "percent"})
Mexico['ctryname']='Mexico'

#merge = China.append(Mexico, ignore_index=True)
'''

hts6_data = data_p[data_p.hts6 == '170410']

sns.set(style="darkgrid")
fig, ax1 = plt.subplots(figsize=(15, 7))
ax2 = ax1.twinx()  # set up the 2nd axis

ax1.scatter(hts6_data.year, hts6_data.ChinaM, color='r', s=hts6_data.China_per, label='China')

#plot the share on axis #2
ax2.scatter(hts6_data.year, hts6_data.MexicoM, color='g', s=hts6_data.Mexico_per, label='Mexico')

plt.title('CHEWING GUM, WHETHER OR NOT SUGAR COATED (170410)')
ax1.set_ylabel('Imports for Consumption (Millions of US Dollars) from China')
ax2.set_ylabel('Imports for Consumption (Millions of US Dollars) from Mexico')
ax1.set_xlabel('Year');
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=2)
ax1.grid()

#plt.show()

plt.savefig(vfolder + r'\scatter_170410.png')

plt.close()