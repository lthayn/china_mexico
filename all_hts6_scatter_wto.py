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


post_wto_2 = post_wto_2[post_wto_2.ctryname != 'total']
post_wto_2 = post_wto_2.drop(['description'], axis=1)
post_wto_p = post_wto_2.pivot(index=['year', 'hts6'], columns='ctryname', values='value').reset_index()
post_wto_p = post_wto_p.fillna(0)
post_wto_p['ChinaM'] = post_wto_p['China']/1000000000
post_wto_p['MexicoM'] = post_wto_p['Mexico']/1000000000

pre_wto_2 = pre_wto_2[pre_wto_2.ctryname != 'total']
pre_wto_2 = pre_wto_2.drop(['description'], axis=1)
pre_wto_p = pre_wto_2.pivot(index=['year', 'hts6'], columns='ctryname', values='value').reset_index()
pre_wto_p = pre_wto_p.fillna(0)
pre_wto_p['ChinaM'] = pre_wto_p['China']/1000000000
pre_wto_p['MexicoM'] = pre_wto_p['Mexico']/1000000000


#post scatter
sns.set(style="darkgrid")
fig, ax = plt.subplots(figsize=(15, 10))

ax.scatter(post_wto_p["ChinaM"], post_wto_p["MexicoM"])

m, b = np.polyfit(post_wto_p["ChinaM"], post_wto_p["MexicoM"], 1)

plt.plot(post_wto_p["ChinaM"], m*post_wto_p["ChinaM"] + b, color='red')
plt.title('After China joined WTO')
ax.set_ylabel('Imports for Consumption (Millions of US Dollars) from Mexico')
ax.set_xlabel('Imports for Consumption (Millions of US Dollars) from China');

plt.savefig(r'Z:\...\post_scatter.png')

plt.close()

#pre scatter
sns.set(style="darkgrid")
fig, ax = plt.subplots(figsize=(15, 10))

ax.scatter(pre_wto_p["ChinaM"], pre_wto_p["MexicoM"])

m, b = np.polyfit(pre_wto_p["ChinaM"], pre_wto_p["MexicoM"], 1)

plt.plot(pre_wto_p["ChinaM"], m*pre_wto_p["ChinaM"] + b, color='red')
plt.title('Before China joined WTO')
ax.set_ylabel('Imports for Consumption (Millions of US Dollars) from Mexico')
ax.set_xlabel('Imports for Consumption (Millions of US Dollars) from China');

plt.savefig(r'Z:\...\pre_scatter.png')

plt.close()