import pandas as pd
from scipy.stats import pearsonr
import numpy as np

folder=r'Z:\...'

#post wto data
post_wto = pd.read_excel (folder + r'\hts6_data.xlsx', sheet_name='2001_to_2019',
                             converters={'hts6':str})
post_wto = post_wto[post_wto.ctryname != 'total']
post_wto = post_wto.fillna(0)

#remove columns were years have no value
#post_wto['sum'] = post_wto.iloc[:, 3:].sum(axis=1)
#post_wto =post_wto[post_wto['sum'] >= 0]



#pre wto data
pre_1996_2000 = pd.read_excel (folder + r'\hts6_data.xlsx', sheet_name='1996_to_2000',
                             converters={'hts6':str})
pre_1996_2000 = pre_1996_2000[pre_1996_2000.ctryname != 'total']

pre_1989_1995 = pd.read_excel (folder + r'\hts6_data.xlsx', sheet_name='1989_to_1995',
                             converters={'hts6':str})
pre_1989_1995 = pre_1989_1995[pre_1989_1995.ctryname != 'total']

pre_wto = pre_1989_1995.merge(pre_1996_2000, how='outer', on=['hts6', 'ctryname', 'description'])
pre_wto = pre_wto.fillna(0)


#remove columns were years have no value
#post_wto['sum'] = post_wto.iloc[:, 3:].sum(axis=1)
#post_wto =post_wto[post_wto['sum'] >= 0]


#definition
definition = post_wto[["hts6", "description"]].copy()
definition.drop_duplicates(subset=['hts6'], keep='first', inplace=True)

#prep list of hts6 numbers to iterate over
numbers = pd.read_excel (folder + r'\hts8_numbers.xlsx', converters={'hts8':str})
numbers['hts6'] = numbers['hts8'].str[:6]
numbers = numbers.drop(['hts8'], axis=1)
numbers.drop_duplicates(subset=['hts6'], keep='first', inplace=True)
hts6 = numbers['hts6'].to_list()



def correlation (chapter, input):
    #get chapter, drop unneeded columns
    file = input.loc[input['hts6'] == chapter]
    file = file.drop(['hts6'], axis=1)
    file = file.drop(['description'], axis=1)
    #reindex, remove old index
    file = file.reset_index().set_index('ctryname')
    file = file.drop(['index'], axis=1)
    #pivot table
    file_t = file.T
    #calculate correlations
    pearson = file_t['China'].corr(file_t['Mexico'], method="pearson")
    kendall = file_t['China'].corr(file_t['Mexico'], method="kendall")
    spearman = file_t['China'].corr(file_t['Mexico'], method="spearman")
    #create dataframe
    df = pd.DataFrame([[chapter, pearson, kendall, spearman]], columns=['hts6', 'pearson', 'kendall', 'spearman'])
    return df


#this creates a dataframe with all the correlations of each hts6 - post wto
post_correlation_data = df = pd.DataFrame(columns = ['hts6', 'pearson', 'kendall', 'spearman'])

for i in hts6:
    try:
        post_correlation_data = post_correlation_data.append(correlation(i, post_wto))
    except:
        pass

#this creates a dataframe with all the correlations of each hts6 - pre wto
pre_correlation_data = df = pd.DataFrame(columns = ['hts6', 'pearson', 'kendall', 'spearman'])

for i in hts6:
    try:
        pre_correlation_data = pre_correlation_data.append(correlation(i, pre_wto))
    except:
        pass


correlation_data = pre_correlation_data.merge(post_correlation_data, how="outer", on="hts6", suffixes=("_pre_wto", "_post_wto"))


#merges definitions into correlation coefficients
correlation_data = correlation_data.merge(definition, how='left', on=['hts6'])

columns = ['hts6', 'description', 'pearson_pre_wto', 'kendall_pre_wto', 'spearman_pre_wto',
       'pearson_post_wto', 'kendall_post_wto', 'spearman_post_wto']

correlation_data = correlation_data[columns]

correlation_data.to_excel(folder +r'\hts6_correlation.xlsx')