import pandas as pd
import numpy as np
from sklearn import linear_model
import statsmodels.api as sm
import matplotlib.pyplot as plt

folder=r'Z:\...'
vfolder=r'Z:\...'

post_wto = pd.read_excel (folder + r'\hts6_data.xlsx', sheet_name='2001_to_2019',
                             converters={'hts6':str})
post_wto_2 = pd.melt(post_wto, id_vars=['ctryname', 'hts6', 'description'], value_vars=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
                                                                                        2013, 2014, 2015, 2016, 2017, 2018, 2019])
post_wto_2 = post_wto_2.rename(columns={"variable": "year"})
post_wto_2['wto'] = 1
post_wto_2['nafta'] = 1

pre_1996_2000 = pd.read_excel (folder + r'\hts6_data.xlsx', sheet_name='1996_to_2000',
                             converters={'hts6':str})

pre_1989_1995 = pd.read_excel (folder + r'\hts6_data.xlsx', sheet_name='1989_to_1995',
                             converters={'hts6':str})


pre_wto = pre_1989_1995.merge(pre_1996_2000, how='outer', on=['ctryname', 'hts6', 'description'])


pre_wto_2 = pd.melt(pre_wto, id_vars=['ctryname', 'hts6', 'description'], value_vars=[1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000])
pre_wto_2 = pre_wto_2.rename(columns={"variable": "year"})
pre_wto_2["wto"] = 0
pre_wto_2['nafta'] = np.where(pre_wto_2["year"].ge(1992), 1, 0)



data = pd.concat([post_wto_2, pre_wto_2])
data = data.drop(['description'], axis=1)

data_p = data .pivot(index=['year', 'hts6', 'wto', 'nafta'], columns='ctryname', values='value').reset_index()
data_p= data_p.fillna(0)

#variable creation
data_p['China_per'] = data_p['China']/data_p['total']*100
data_p['Mexico_per'] = data_p['Mexico']/data_p['total']*100

data_p["wto * China"] = data_p['wto'] * data_p['China']

data_p["China * China"] = data_p['China'] * data_p['China']


'''
#first example
X = data_p[['wto', 'nafta', 'China']]
Y = data_p['Mexico']


# with sklearn
regr = linear_model.LinearRegression()
regr.fit(X, Y)

# with statsmodels
X = sm.add_constant(X)  # adding a constant

model = sm.OLS(Y, X).fit()
predictions = model.predict(X)

print_model = model.summary()
print(print_model)

plt.rc('figure', figsize=(12, 7))
#plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 12}) old approach
plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, fontproperties = 'monospace') # approach improved by OP -> monospace!
plt.axis('off')
plt.tight_layout()
plt.savefig(vfolder + r'\first.png')

#second example


X = data_p[['wto', 'nafta', 'China_per']]
Y = data_p['Mexico_per']
X = X.fillna(0)
Y = Y.fillna(0)

# with statsmodels
X = sm.add_constant(X)  # adding a constant

model = sm.OLS(Y, X).fit()
predictions = model.predict(X)

print_model = model.summary()
print(print_model)

plt.rc('figure', figsize=(12, 7))
#plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 12}) old approach
plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, fontproperties = 'monospace') # approach improved by OP -> monospace!
plt.axis('off')
plt.tight_layout()
plt.savefig(vfolder + r'\percent.png')


#third example

X = data_p[['wto', 'nafta', 'China', 'wto * China']]
Y = data_p['Mexico']


# with sklearn
regr = linear_model.LinearRegression()
regr.fit(X, Y)

# with statsmodels
X = sm.add_constant(X)  # adding a constant

model = sm.OLS(Y, X).fit()
predictions = model.predict(X)

print_model = model.summary()
print(print_model)

plt.rc('figure', figsize=(12, 7))
#plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 12}) old approach
plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, fontproperties = 'monospace') # approach improved by OP -> monospace!
plt.axis('off')
plt.tight_layout()
plt.savefig(vfolder + r'\wto_china.png')
'''
#fourth example

X = data_p[['wto', 'nafta', 'China', 'wto * China', "China * China"]]
Y = data_p['Mexico']


# with sklearn
regr = linear_model.LinearRegression()
regr.fit(X, Y)

# with statsmodels
X = sm.add_constant(X)  # adding a constant

model = sm.OLS(Y, X).fit()
predictions = model.predict(X)

print_model = model.summary()
print(print_model)

plt.rc('figure', figsize=(12, 7))
#plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 12}) old approach
plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, fontproperties = 'monospace') # approach improved by OP -> monospace!
plt.axis('off')
plt.tight_layout()
plt.savefig(vfolder + r'\China_china.png')


#fifth example

X = data_p[['wto', 'nafta', 'China', "China * China"]]
Y = data_p['Mexico']


# with sklearn
regr = linear_model.LinearRegression()
regr.fit(X, Y)

# with statsmodels
X = sm.add_constant(X)  # adding a constant

model = sm.OLS(Y, X).fit()
predictions = model.predict(X)

print_model = model.summary()
print(print_model)