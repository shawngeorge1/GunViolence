import pandas as pd 
import numpy as np
import json
data = pd.read_csv('gun-violence-data_01-2013_03-2018.csv')
data['cas'] = data['n_killed'] + data['n_injured']
labels = ['date', 'state', 'city_or_county', 'cas']
data = data[labels]
data = data[data['cas'] != 0]
data['date'] = data['date'].apply(lambda x : x.split('-')[0])

data_2014 = data[data['date'] == '2014']
data_2015 = data[data['date'] == '2015']
data_2016 = data[data['date'] == '2016']
data_2017 = data[data['date'] == '2017']
data_2018 = data[data['date'] == '2018']

list_of_states = data_2014['state'].unique()

data_2014 = (data_2014.groupby(['state'])['cas'].sum().reset_index())
data_2015 = (data_2015.groupby(['state'])['cas'].sum().reset_index())
data_2016 = (data_2016.groupby(['state'])['cas'].sum().reset_index())
data_2017 = (data_2017.groupby(['state'])['cas'].sum().reset_index())
data_2018 = (data_2018.groupby(['state'])['cas'].sum().reset_index())

data_set = [data_2014, data_2015, data_2016, data_2017, data_2018]
for d in data_set:
    d['zscore'] = (d['cas'] - d['cas'].mean())/d['cas'].std(ddof=0)

data_2014 = data_2014.set_index('state').to_dict()['zscore']
data_2015 = data_2015.set_index('state').to_dict()['zscore']
data_2016 = data_2016.set_index('state').to_dict()['zscore']
data_2017 = data_2017.set_index('state').to_dict()['zscore']
data_2018 = data_2018.set_index('state').to_dict()['zscore']

states = {}
data_set = [data_2014, data_2015, data_2016, data_2017, data_2018]

for state in list_of_states:
    if not state in states:
        states[state] = []

for data in data_set:
    for state in list_of_states:
            entry = data[state] 
            states[state] = np.append(states[state], entry)

final_array = [None] * 51
i = 0
for state in states:
    final_array[i] = [state, list(states[state])]
    i = i + 1

states = {"states" : final_array}
with open('gun-violence.js', 'w') as outfile:
    json.dump(states, outfile)
