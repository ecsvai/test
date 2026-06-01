import pandas as pd


data = pd.read_csv('23-06kumamoto_main.csv')

data['在留資格'] = data['在留資格'].str.replace('?','・',regex=True)



data.to_excel('23-06kumamoto_maintest.xlsx', index=False)