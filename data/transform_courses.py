import pandas as pd

df = pd.read_json('data\\courses.json')

#Save as csv
df.to_csv('data\\courses.csv', index=False)

print(df.head())