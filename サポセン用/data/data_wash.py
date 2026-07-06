import pandas as pd


df = pd.read_csv('21-06kumamoto_main.csv')

df = df.drop(['Unnamed: 0.1','Unnamed: 0.2'],axis=1)

df.to_csv('21-06kumamoto_main.csv', index=False)


