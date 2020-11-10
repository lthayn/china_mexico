import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

folder = r'Z:\...'
file = r'\....xlsx'
link =  folder + file

vfolder=r'Z:\...'

#read data
data = pd.read_excel(link, sheet_name='GDP_Cap_constant', skiprows=[0, 1, 2, 3, 5])

#prep dataset
data = data.rename(columns={"YEAR": "ctry_name"}, errors="raise")

data['ctry_name'] = data['ctry_name'].str.strip()

#subset data
data2 = data.loc[(data['ctry_name'] == 'China') | (data['ctry_name'] == 'Mexico')]
data2 = data2.set_index('ctry_name')

data_transpose = data2.T


#graph
sns.set(style="darkgrid")
fig, ax = plt.subplots(figsize=(15, 7))


ax.plot(data_transpose.index, data_transpose.China, 'r', linewidth=3, label='China')
ax.plot(data_transpose.index, data_transpose.Mexico, 'g', linewidth=3, label="Mexico")
plt.xticks(data_transpose.index, rotation='vertical')
ax.set_ylabel('Gross domestic product per capita (US dollars at constant prices (2010)');
ax.set_xlabel('Year');
plt.legend(title='Countries')

#plt.show()
plt.savefig(vfolder + r'\GDP_capita.png')

plt.close()