import pandas as pd


df = pd.read_excel('25-06年齢・性別別.xlsx', header=3)
df_new = df.copy()


df_new.loc[df['州']=='無国籍','国籍・地域']='無国籍'

df_new.to_excel('test!!!!!!!!!.xlsx', index=False)