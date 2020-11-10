import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file = r'\GDP_PPP.xlsx'
folder = r'Z:\...'
link =  folder + file

vfolder=r'Z:\...'

data = pd.read_excel(link, skiprows=[0, 1, 2])

#print(data.columns)
#print(data['Country Name'])

data = data.rename(columns={"Country Name": "ctry_name", "Country Code": "ctry_code",
                            "Indicator Name":  "indicator", "Indicator Code": "ind_code"})

data = data.set_index('ctry_name')


data2=data.loc[['China', 'Mexico'], :]


data2=data2.drop(['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972',
                  '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1984',
                  '1985', '1986', '1987', '1988', '1989', '2019'], axis=1)
#print(years)

columns = ['ctry_code', 'indicator', 'ind_code']
data2.drop(columns, inplace=True, axis=1)

data_transpose = data2.T

data_transpose['China'] = data_transpose['China']/1000000000000
data_transpose['Mexico'] = data_transpose['Mexico']/1000000000000
#data_transpose['World'] = data_transpose['World']/1000000000


#print(data_transpose)

sns.set(style="darkgrid")
fig, ax = plt.subplots(figsize=(15, 7))


ax.plot(data_transpose.index, data_transpose.China, 'r', linewidth=3, label='China')
ax.plot(data_transpose.index, data_transpose.Mexico, 'g', linewidth=3, label="Mexico")
ax.set_ylabel('GDP, PPP (Billion USD $)');
ax.set_xlabel('Year');
plt.legend(title='Countries')

#plt.show()
plt.savefig(vfolder + r'\GDP_PPP.png')

plt.close()