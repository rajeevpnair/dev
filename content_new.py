import pandas as pd

pd.set_option('display.expand_frame_repr', False)
df = pd.read_html('test.html')
df = df[0].dropna(axis=0, thresh=4)
df.columns = df.iloc[0]
df = df.loc[df['Status'] == 'Failed']
print (df)
n = (df.shape[0])
i = 0
print (df.iat[2,3])

while (i < n):
	description = (df.iat[i,0], ' ', df.iat[i,2], 'for', ' ', df.iat[i,1] )
	description = ''.join(description)
	print (description)
	i = i + 1
