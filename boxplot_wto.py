import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

folder=r'Z:\...'
vfolder=r'Z:\...'

post_wto = pd.read_excel (folder + r'\hts8_data.xlsx', sheet_name='2001_to_2019',
                             converters={'hts8':str})
post_wto_2 = pd.melt(post_wto, id_vars=['ctryname', 'hts8', 'description'], value_vars=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
                                                                                        2013, 2014, 2015, 2016, 2017, 2018, 2019])
post_wto_2 = post_wto_2.rename(columns={"variable": "year"})
post_wto_2['wto'] = 1

pre_1996_2000 = pd.read_excel (folder + r'\hts8_data.xlsx', sheet_name='1996_to_2000',
                             converters={'hts8':str})

pre_1989_1995 = pd.read_excel (folder + r'\hts8_data.xlsx', sheet_name='1989_to_1995',
                             converters={'hts8':str})


pre_wto = pre_1989_1995.merge(pre_1996_2000, how='outer', on=['ctryname', 'hts8', 'description'])


pre_wto_2 = pd.melt(pre_wto, id_vars=['ctryname', 'hts8', 'description'], value_vars=[1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000])
pre_wto_2 = pre_wto_2.rename(columns={"variable": "year"})
pre_wto_2["wto"] = 0

data_t = pd.concat([post_wto_2, pre_wto_2])

data_t = data_t[data_t.ctryname != 'total']


data_t.to_excel(folder +r'\hts8_transposed.xlsx')

grouped_data = data_t.groupby(['ctryname','year','wto'])['value'].sum().reset_index()



sns.set(style="darkgrid")
fig, ax = plt.subplots(figsize=(8, 5))

g = sns.boxplot(x="ctryname", y="value", hue="wto", data=grouped_data, palette="Set2", showfliers=False)

ax.set_ylabel('Imports for Consumption (Billions $)');
ax.set_xlabel('Country');

#g.legend(bbox_to_anchor=(1, 1), ncol=1)
#g.set(xlim = (50000,250000))
ylabels = ['{:,.2f}'.format(x) + 'B' for x in g.get_yticks()/1000000000]
g.set_yticklabels(ylabels)

#plt.show()

plt.savefig(vfolder + r'\box_plot.png')

plt.close()
