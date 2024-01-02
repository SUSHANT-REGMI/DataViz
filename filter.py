#Age and Rating filter
import pandas as pd

file_path = 'bookrec.csv'
encoding_type = 'latin-1'  

df = pd.read_csv(file_path, encoding=encoding_type)

df.loc[df['age'] > 80, 'age'] = 'N/A'
df.loc[df['book_rating'] == 0, 'book_rating'] = 'N/A'


df.to_csv(file_path, index=False, encoding=encoding_type)


