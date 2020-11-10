import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

folder = r'Z:\...'
file = r'\....xlsx'
link =  folder + file

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
#creating percentages
data_p['China_per'] = data_p['China']/data_p['total']*100
data_p['Mexico_per'] = data_p['Mexico']/data_p['total']*100

# set width of bar
labels = data_p.index.to_list()
width = 0.30
x = np.arange(len(labels))  # the label locations

# Set position of bar on X axis
r1 = labels
r2 = [x + width for x in r1]
r3 = [x + width for x in r2]

sns.set(style="white", rc={'figure.figsize': (25, 8)})
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()  # set up the 2nd axis

ax1.bar(r1, data_p.totalM, width=width, color='b', label='Value from the World')
ax1.bar(r2, data_p.MexicoM, width=width, color='green', label='Value from Mexico')
ax1.bar(r3, data_p.ChinaM, width=width, color='r', label='Value from China')

#plot the share on axis #2
ax2.plot(data_p.index, data_p.China_per, linewidth=3, color='r', label='Share from China')
ax2.plot(data_p.index, data_p.Mexico_per, linewidth=3, color='green', label='Share from Mexico')
#ax2.plot(data2.index, data2.Germany, linewidth=3, color='skyblue', label='Share from Germany')
#ax2.plot(data2.index, data2.Other, linewidth=3, color='yellow', label='Share from other sources')

ax1.set_ylabel('Imports for Consumption (Billions of US Dollars)')
ax2.set_ylabel('Share of Imports for Consumption(Percent)')
ax1.set_xlabel('Year');

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2)
ax1.grid()

plt.savefig(r'Z:\....\total_line_bar.png')

plt.close()